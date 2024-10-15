import os
import socket
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
INTERNAL_IPS = ['127.0.0.1', ]

ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1"]

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = os.getenv("DJANGO_DEBUG", "") != "False"

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "debug_toolbar",
    "corsheaders",
    "rest_framework",
    "user",
    "comments",
    "captcha"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                f"redis://{os.getenv('REDIS_HOST', 'redis')}:6379/2"
            ],
        },
    },
}

WSGI_APPLICATION = 'comments_spa.wsgi.application'
ASGI_APPLICATION = 'comments_spa.asgi.application'


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080"
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "comments_spa.urls"

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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}


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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": os.getenv("COMMENTS_PAGE_SIZE", 25),
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MAX_FILE_SIZE_KB = os.getenv("MAX_FILE_SIZE_KB", 100)
MAX_IMAGE_WIDTH_KB = os.getenv("MAX_IMAGE_WIDTH_KB", 320)
MAX_IMAGE_HEIGHT_KB = os.getenv("MAX_IMAGE_HEIGHT_KB", 240)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=float(os.getenv("ACCESS_TOKEN_LIFETIME", 30))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        minutes=float(os.getenv("REFRESH_TOKEN_LIFETIME", 60 * 24))
    )
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST', 'redis')}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CELERY_BROKER_URL = f"redis://{os.getenv('REDIS_HOST', 'redis')}:6379/0"
CELERY_TIMEZONE = "UTC"

CAPTCHA_TTL = int(os.getenv("CAPTCHA_TTL", 300))
CAPTCHA_LENGTH = int(os.getenv("CAPTCHA_LENGTH", 5))

CACHE_TTL = int(os.getenv("CACHE_TTL", 300))
REPLIES_PAGE_SIZE = int(os.getenv("REPLIES_PAGE_SIZE", 10))

