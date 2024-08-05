from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import random
import string
from .settings import accounts_config
from .models import EmailAddress, EmailConfirmationCode
from importlib import import_module


def set_cookies(
    response, access_token=None, refresh_token=None, mfa=None, email_verification=None
):
    """
    Set a cookie on the response.

    Parameters:
    - response (HttpResponse): The response object to set the cookie on.
    - access_token (str): The access token.
    - refresh_token (str): The refresh token.
    - mfa (str): The id of the user that is used to authenticate after MFA authentication.
    """
    access_token_lifetime = settings.SIMPLE_JWT.get(
        "ACCESS_TOKEN_LIFETIME"
    ).total_seconds()
    refresh_token_lifetime = settings.SIMPLE_JWT.get(
        "REFRESH_TOKEN_LIFETIME"
    ).total_seconds()

    if access_token:
        response.set_cookie(
            accounts_config["ACCESS_TOKEN_COOKIE_NAME"],
            access_token,
            max_age=int(access_token_lifetime),
            path=accounts_config["COOKIE_PATH"],
            domain=accounts_config["COOKIE_DOMAIN"],
            secure=accounts_config["COOKIE_SECURE"],
            httponly=accounts_config["COOKIE_HTTP_ONLY"],
            samesite=accounts_config["COOKIE_SAMESITE"],
        )

    if refresh_token:
        response.set_cookie(
            accounts_config["REFRESH_TOKEN_COOKIE_NAME"],
            refresh_token,
            max_age=int(refresh_token_lifetime),
            path=accounts_config["COOKIE_PATH"],
            domain=accounts_config["COOKIE_DOMAIN"],
            secure=accounts_config["COOKIE_SECURE"],
            httponly=accounts_config["COOKIE_HTTP_ONLY"],
            samesite=accounts_config["COOKIE_SAMESITE"],
        )
    if mfa:
        response.set_cookie(
            accounts_config["MFA_COOKIE_NAME"],
            mfa,
            max_age=accounts_config["MFA_COOKIE_LIFETIME"].total_seconds(),
            path=accounts_config["COOKIE_PATH"],
            domain=accounts_config["COOKIE_DOMAIN"],
            secure=accounts_config["COOKIE_SECURE"],
            httponly=accounts_config["COOKIE_HTTP_ONLY"],
            samesite=accounts_config["COOKIE_SAMESITE"],
        )

    return response


def dispatch_email(context, email, subject, template):
    """
    Sends an email to the sepcified email

    Args:
        context (any): The context of the email which will be passed to the template
        email (str): The email address to which the email will be sent
        subject (str): The subject of the email
        template (str): The name of the template located in the 'emails' folder
    """
    context["PLATFORM_NAME"] = accounts_config["PLATFORM_NAME"]
    template_name = f"emails/{template}.html"
    convert_to_html_content = render_to_string(
        template_name=template_name, context=context
    )
    plain_message = strip_tags(convert_to_html_content)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            email,
        ],
        html_message=convert_to_html_content,
        fail_silently=True,
    )


def handle_email_verification(user):
    """
    Generates a confirmation code with a mix of letters and numbers.


    Returns:
    - str: The generated confirmation code.
    """
    length = accounts_config["CONFIRMATION_CODE_LENGTH"]
    if length < 2:
        raise ValueError(
            "Length must be at least 2 to include both letters and numbers."
        )

    letters = random.sample(string.ascii_letters, 1)  # Ensure at least one letter
    numbers = random.sample(string.digits, 1)  # Ensure at least one number
    remaining_chars = random.choices(string.ascii_letters + string.digits, k=length - 2)

    # Combine and shuffle to ensure randomness
    code_chars = letters + numbers + remaining_chars
    random.shuffle(code_chars)

    code = "".join(code_chars)
    try:
        user_code, created = EmailConfirmationCode.objects.get_or_create(user=user)
        user_code.code = code
        user_code.save()
        dispatch_email(
            subject="Email Verification",
            email=user.email,
            template="verify_email",
            context={"code": code},
        )
    except Exception as e:
        raise ValueError(f"Could not create a confirmation code. Error: {e}")
    return user_code


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def generate_password_reset_code():
    digits = random.choice(string.digits)
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)

    # Generate the remaining 3 characters randomly from all allowed characters
    remaining_characters = string.ascii_letters + string.digits
    remaining = "".join(random.choice(remaining_characters) for _ in range(3))

    # Combine all characters and shuffle
    code_list = list(digits + uppercase + lowercase + remaining)
    random.shuffle(code_list)

    return "".join(code_list)


def get_serializer(path):
    """Dynamically import and return serializer"""

    serializer_module, serializer_class = path.rsplit(".", 1)
    module = import_module(serializer_module)
    return getattr(module, serializer_class)


def user_email_address(user):
    email_address, created = EmailAddress.objects.get_or_create(user=user, primary=True)

    if created:
        email_address.primary = True
        email_address.email = user.email
        email_address.save()

    return email_address


def reset_response(response):
    response.delete_cookie(accounts_config["ACCESS_TOKEN_COOKIE_NAME"])
    response.delete_cookie(accounts_config["REFRESH_TOKEN_COOKIE_NAME"])
