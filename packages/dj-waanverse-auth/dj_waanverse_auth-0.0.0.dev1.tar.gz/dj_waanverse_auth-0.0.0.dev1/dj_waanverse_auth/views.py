from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    LoginSerializer,
    ReVerifyEmailSerializer,
    VerifyEmailSerializer,
    MfaCodeSerializer,
    LogoutSerializer,
    ResetPasswordSerializer,
    VerifyResetPasswordSerializer,
)
from django.contrib.auth import user_logged_in
from rest_framework.permissions import AllowAny
from .utils import set_cookies, get_serializer, reset_response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import pyotp
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from .settings import accounts_config
from .models import MultiFactorAuth

Account = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    USER_CLAIM_SERIALIZER = get_serializer(accounts_config["USER_CLAIM_SERIALIZER"])
    # Any changes to the main login view may affect the mfa login view
    serializer = LoginSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        mfa = serializer.validated_data.get("mfa", False)
        refresh_token = serializer.validated_data.get("refresh_token", "")
        access_token = serializer.validated_data.get("access_token", "")
        user = serializer.validated_data.get("user", None)
        email_verified = serializer.validated_data.get("email_verified", False)
        if mfa is True:
            response = Response(status=status.HTTP_200_OK, data={"mfa": user.id})
            response = set_cookies(mfa=user.id, response=response)
            reset_response(response)
        elif email_verified is False:
            response = Response(
                {"email": user.email, "status": "unverified"}, status=status.HTTP_200_OK
            )
            reset_response(response)
        else:
            response = Response(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": USER_CLAIM_SERIALIZER(user).data,
                },
                status=status.HTTP_200_OK,
            )

            response = set_cookies(
                response, access_token=access_token, refresh_token=refresh_token
            )
        return response
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token_view(request):
    refresh_token = request.data.get("refresh") or request.COOKIES.get(
        accounts_config["REFRESH_TOKEN_COOKIE_NAME"]
    )

    if not refresh_token:
        return Response(
            {"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        refresh = RefreshToken(refresh_token)
        # Generate a new access token
        new_access_token = str(refresh.access_token)
        # Return the new access token in the response
        response = Response({"access": new_access_token}, status=status.HTTP_200_OK)
        new_response = set_cookies(access_token=new_access_token, response=response)
        return new_response
    except TokenError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def reverify_email(request):
    """
    Collect email from the user to resend the verification email.
    """
    serializer = ReVerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.save()
        return Response(
            {"email": email},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_email(request):
    """
    Verify email
    """
    serializer = VerifyEmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        return Response(
            {"email": email, "status": "verified"}, status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    SignupSerializer = get_serializer(accounts_config["SIGNUP_SERIALIZER"])
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        response = Response(
            {
                "email": user.email,
                "status": "unverified",
            },
            status=status.HTTP_201_CREATED,
        )

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def enable_mfa(request):
    try:
        user = request.user
        account_mfa, created = MultiFactorAuth.objects.get_or_create(account=user)

        if not account_mfa.secret_key:
            # Ensure the generated key is unique
            while True:
                potential_key = pyotp.random_base32()
                if not MultiFactorAuth.objects.filter(
                    secret_key=potential_key
                ).exists():
                    account_mfa.secret_key = potential_key
                    break

        otp_url = pyotp.totp.TOTP(account_mfa.secret_key, digits=6).provisioning_uri(
            user.username, issuer_name=accounts_config["MFA_ISSUER"]
        )

        account_mfa.save()

        return Response(
            {"url": otp_url, "key": account_mfa.secret_key}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})


@api_view(["POST"])
def verify_mfa(request):
    user = request.user
    try:
        mfa_account = MultiFactorAuth.objects.get(account=user)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
    if mfa_account.activated:
        return Response({"msg": "MFA already activated"}, status=status.HTTP_200_OK)

    serializer = MfaCodeSerializer(data=request.data)

    if serializer.is_valid():
        code = serializer.validated_data.get("code")
        totp = pyotp.TOTP(mfa_account.secret_key)

        if totp.verify(code):
            mfa_account.activated = True
            mfa_account.set_recovery_codes()
            mfa_account.save()
            return Response(
                {"msg": "2FA enabled successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response({"msg": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def mfa_activated(request):
    recovery_code = request.user.recovery_codes
    return Response(data={"recovery_codes": recovery_code}, status=status.HTTP_200_OK)


@api_view(["POST"])
def regenerate_recovery_codes(request):
    request.user.set_recovery_codes()
    request.user.save()
    return Response(
        status=status.HTTP_200_OK, data={"msg": "Codes generated successfully"}
    )


@api_view(["POST"])
def deactivate_mfa(request):
    user = request.user
    password = request.data.get("password")

    if not password:
        return Response(
            {"msg": "Please provide us with a valid password to continue."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user.check_password(password):
        user.mfa_activated = False
        user.mfa_secret = None
        user.save()
        return Response(
            {"msg": "Multi-factor authentication has been deactivated successfully"},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"msg": "Incorrect password please try again."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def user_info(request):
    AccountSerializer = get_serializer(accounts_config["USER_DETAIL_SERIALIZER"])
    user = request.user
    serializer = AccountSerializer(user)
    print("called")
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout_view(request):
    serializer = LogoutSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        try:
            serializer.save()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        logout(request)

        response = Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )

        # Clear cookies
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def mfa_login(request):
    user_id = request.COOKIES.get(accounts_config["MFA_COOKIE_NAME"])
    User_Claim_Serializer = get_serializer(accounts_config["USER_CLAIM_SERIALIZER"])
    refresh = None
    access = None
    if not user_id:
        return Response(
            {
                "msg": "Unable to verify your account. Please login again.",
                "invalid_account": True,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = Account.objects.get(pk=user_id)
        mfa_account = MultiFactorAuth.objects.get(account=user)
    except Account.DoesNotExist:
        return Response({"msg": "Invalid account"}, status=status.HTTP_400_BAD_REQUEST)

    if not mfa_account.activated:
        return Response(
            {"msg": "MFA is not activated for this user"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    code = request.data.get("code", 0)
    totp = pyotp.TOTP(mfa_account.secret_key)

    if totp.verify(code):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

    elif code in user.recovery_codes:
        # Recovery code is valid
        mfa_account.recovery_codes.remove(code)  # Remove used recovery code
        mfa_account.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
    else:
        return Response(
            {"msg": "Invalid OTP or recovery code"}, status=status.HTTP_400_BAD_REQUEST
        )

    update_last_login(None, user)
    user_logged_in.send(
        sender=user.__class__,
        request=request,
        user=user,
    )

    response = Response(
        {
            "refresh": str(refresh),
            "access": str(access),
            "user": User_Claim_Serializer(user).data,
        },
        status=status.HTTP_200_OK,
    )

    response = set_cookies(
        response=response, access_token=access, refresh_token=refresh
    )
    response.delete_cookie(accounts_config["MFA_COOKIE_NAME"])

    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        reset_code = serializer.save()
        attempts = reset_code.attempts
        email = reset_code.email
        return Response(
            status=status.HTTP_200_OK,
            data={
                "msg": "Password reset successfully",
                "attempts": attempts,
                "email": email,
            },
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_reset_password(request):
    serializer = VerifyResetPasswordSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": _("Password has been reset successfully.")},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
