import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-scssi7n202#51%j5^tn9w0z(mvnda!l7i6@9!do!vz6&h97tvo"

# Stripe Settings
STRIPE_PUBLISHABLE_KEY = "pk_test_51OC0oNFFtkobwiNu4uT0IZmqdeLhYeqdW0mDifhQUlZg0RNDZ9iMiHGyHEDgs3IvPDalzrvK31qX6gPk2jamlLzN00b3grbeWo"  # Publishable key
STRIPE_SECRETKEY = "sk_test_51OC0oNFFtkobwiNuu1cpSqsKQzlgDEfiHkF3Cp3xNqFt00xgaWNABtnag2IYpbQX8tmbFy9duYV6XoK2sfwqQWDx00xzgSN1VV"  # Secret key
STRIPE_API_VERSION = "2022-08-01"

# LocationIQ CONFIG
LOCATIONIQ_KEY = "pk.4db5adc620aaca2d5b1f7096b5122be4"
LOCATIONIQ_API = (
    f"https://eu1.locationiq.com/v1/reverse?key={LOCATIONIQ_KEY}&format=json"
)

# Agora CONFIG Mobader
# AGORA_APP_ID = "21c0c5c07a0b4c0da0e7f53ab427ee7f"

# Agora CONFIG Abdelrahman
AGORA_APP_ID = "50e83f3fb06241789551baa20de1f56b"

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = False
# ALLOWED_HOSTS = ["mobader.sa", "www.mobader.sa"]
DEBUG = True
ALLOWED_HOSTS = ["2752-102-185-153-196.ngrok-free.app", '*']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local
    "mobaderapp",
    "doctor",
    "patient",
    "nurse",
    "physiotherapist",
    "lab",
    "pharma",
    "chatroom",
    # Libraries
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "drf_spectacular",
]

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "sedrahcare.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sedrahcare.wsgi.application"

# CORS WHITELIST
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "https://relaxed-curie-e9a516.netlify.app",
    "http://127.0.0.1:8080",
]

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^https://\w+\.netlify\.app$",
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mobader",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "adminsedrahcare_mobader",
        "USER": "adminsedrahcare_mobader_user",
        "PASSWORD": "AdminMobader123456",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

"""


REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


COUNTRIES = (("Saudi Arabia", "Saudi Arabia"),)

CITIES = (("AlRiyadh", "AlRiyadh"), ("AlDamam", "AlDamam"), ("Gadah", "Gadah"))

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "mobaderapp.CustomUser"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# SMTP

DEFAULT_FROM_EMAIL = "admin@mobader.sa"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

from django.utils.translation import gettext_lazy as _

LANGUAGES = (
    ("ar", _("Arabic")),
    ("en", _("English")),
)
MULTILINGUAL_LANGUAGES = (
    "en-us",
    "ar-ae",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
"""
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

"""
STATIC_URL = "/static/"
STATIC_ROOT = "/home/adminsedrahcare/public_html/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/adminsedrahcare/public_html/media"


LOGIN_URL = "/user/login"
LOGIN_REDIRECT_URL = "/user/dashboard/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# OTP

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "admin@mobader.sa"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "adminsedrahcare"
EMAIL_HOST_PASSWORD = "MobaderEid123456@"

SPECTACULAR_SETTINGS = {
    "TITLE": "Mobader API V1",
}

# R3YUD7QY6S63LKAPYWRA5KWK Twilio Recovery Code
