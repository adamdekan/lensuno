"""
Django settings for shootbe project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import datetime

# anti broken pipe error
from django.core.servers.basehttp import WSGIServer

WSGIServer.handle_error = lambda *args, **kwargs: None

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["www.lensuno.com", "lensuno.com", "localhost", "127.0.0.1", "*"]


# Application definition

INSTALLED_APPS = [
    "django_admin_tailwind",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
    "users.apps.UsersConfig",
    "main.apps.MainConfig",
    "portfolio.apps.PortfolioConfig",
    "comments.apps.CommentsConfig",
    "wishlist.apps.WishlistConfig",
    "payment.apps.PaymentConfig",
    "gallery",
    "chat",
    "places",
    "django.contrib.humanize",
    "django.forms",
    "django_extensions",
    "phonenumber_field",
    "babel",  # for phonenumberfield
    "compressor",
    "social_django",
    "crispy_forms",
    "bootstrap_modal_forms",
    "country_list",
    "django_htmx",
    "django_filters",
    "crispy_bootstrap4",
    "sorl.thumbnail",  # galleryfield
    "galleryfield",  # galleryfield
    "widget_tweaks",  # https://pypi.org/project/django-widget-tweaks/
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.apple",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "shootbe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "html"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "gallery.utils.static_context_processor",
                "main.context_processors.forms",
            ],
            "builtins": [
                "main.templatetags.shootbe_tags",
                "wishlist.templatetags.wishlist_tags",
            ],
        },
    },
]

WSGI_APPLICATION = "shootbe.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "lensuno_abase",
        "USER": os.environ["POSTGRE_USER"],
        "PASSWORD": os.environ["POSTGRE_PASS"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "CET"

USE_I18N = True

USE_TZ = True

COMPRESS_OFFLINE = True
LIBSASS_OUTPUT_STYLE = "compressed"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

COMPRESS_ROOT = BASE_DIR / "static"
STATIC_ROOT = BASE_DIR / "static"
COMPRESS_ENABLED = True


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ["SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"]
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ["SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"]
GOOGLE_MAPS_API_KEY = os.environ["GOOGLE_MAPS_API_KEY"]
PLACES_MAPS_API_KEY = os.environ["PLACES_MAPS_API_KEY"]
PLACES_MAP_WIDGET_HEIGHT = 250
GOOGLE_OAUTH2_CREDENTIALS = {
    "client_id": "645533288604-d4knjqpji4e0otp5ol3s7gh5n30e7dbo.apps.googleusercontent.com",
    "project_id": "lens-uno",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": os.environ["CLIENT_SECRET"],
    "javascript_origins": ["https://www.lensuno.com"],
    "access_token": "ya29.a0Ael9sCOILSiRU8NObA6Ecemx3j9Q5ZqJPOEvw196bfmNG5M1mfy7uS4air1Wg1B-BVVPE9c0oQ1SViI4ABWAxN-oJ6h8q05d4FEPmkM6zwl6XWMRYmhLOgfEJR0oXj8SPUYLvmMPspMBqO-gYXYvJFAtvjoTaCgYKAQgSARMSFQF4udJhYatqPcCtc7rZjrqY9iBFKA0163",
    "token_expiry": datetime.datetime.now(),
    "user_agent": None,
    "refresh_token": "1//09JJzS-Yhi7vGCgYIARAAGAkSNwF-L9IrkskMLU0l8Mf3kYwbvC46xHQE6ccjtni-v18AdOZjzds994RuKYNaV_xEmaekekyso9s",
    "scope": "https://www.googleapis.com/auth/drive",
    "token_type": "Bearer",
    "scopes": ["https://www.googleapis.com/auth/calendar"],
}


# email configs
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]  # ! use str(os.getenv('EMAIL_USER'))
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

SITE_ID = 1

# allauth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_FORMS = {
    "login": "users.forms.UserSignInForm",
    "signup": "users.forms.UserSignupForm",
    "reset_password": "users.forms.MyCustomResetPasswordForm",
    "change_password": "users.forms.MyCustomChangePasswordForm",
}


# django_resized https://github.com/adamdekan/django-resized
DJANGORESIZED_DEFAULT_SIZE = [700, None]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

# stripe:
STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_API_VERSION = "2022-08-01"


# galler_field
SENDFILE_URL = "/media/protected"
SENDFILE_ROOT = BASE_DIR / "media"
SENDFILE_BACKEND = "django_sendfile.backends.development"
DJANGO_GALLERY_FIELD_CONFIG = {
    "bootstrap_version": 4,
    # "assets": {
    #     "bootstrap_css": "https://cdnjs.cloudflare.com/ajax/libs/"
    #                      "twitter-bootstrap/3.4.1/css/bootstrap.min.css",
    #     "bootstrap_js": "https://cdnjs.cloudflare.com/ajax/libs/"
    #                     "twitter-bootstrap/3.4.1/css/bootstrap.min.js"
    # }
}

STARFIELD_STARS = 10
STARFIELD_COLOUR = "#A13333"