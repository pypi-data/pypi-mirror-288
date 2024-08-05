from django.conf import settings
from datetime import timedelta

DEFAULT_ACCOUNTS_CONFIG = {
    "AUTHENTICATION_METHODS": ["username"],
    "MFA_RECOVERY_CODES_COUNT": 2,
    "ACCESS_TOKEN_COOKIE_NAME": "access",
    "REFRESH_TOKEN_COOKIE_NAME": "refresh",
    "COOKIE_PATH": "/",
    "COOKIE_DOMAIN": None,
    "COOKIE_SAMESITE": "Lax",
    "COOKIE_SECURE": False,
    "COOKIE_HTTP_ONLY": True,
    "MFA_COOKIE_NAME": "mfa",
    "MFA_COOKIE_LIFETIME": timedelta(minutes=2),
    "USER_CLAIM_SERIALIZER": "dj_waanverse_auth.serializers.BasicAccountSerializer",
    "SIGNUP_SERIALIZER": "dj_waanverse_auth.serializers.SignupSerializer",
    "USERNAME_MIN_LENGTH": 4,
    "BLACKLISTED_USERNAMES": ["waanverse"],
    "USER_DETAIL_SERIALIZER": "dj_waanverse_auth.serializers.AccountSerializer",
    "EMAIL_ON_LOGIN": True,
    "ENCRYPTION_KEY": None,
    "CONFIRMATION_CODE_LENGTH": 6,
    "PLATFORM_NAME": "Waanverse Accounts",
    "EMAIL_VERIFICATION_CODE_LIFETIME": timedelta(minutes=10),
    "MFA_ISSUER": "Waanverse Labs Inc.",
}

APP_ACCOUNTS_CONFIG = getattr(settings, "ACCOUNTS_CONFIG", {})

accounts_config = {**DEFAULT_ACCOUNTS_CONFIG, **APP_ACCOUNTS_CONFIG}
