"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# load environment
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]

# Application definition

INSTALLED_APPS = [
    "backend.apps.MyAdminConfig",
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # dependent apps
    "rest_framework",
    "rest_framework.authtoken",
    "phonenumber_field",
    "corsheaders",

    # constructed apps
    "accounts",
    "item",
    "item_group",
    "cart",
    "transaction",
    "reviews"
]

# Rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES'      : [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES'    : [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS'      : 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE'                     : 10
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["accounts"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': os.getenv("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = False

TIME_ZONE = "Asia/Kathmandu"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

MEDIA_URL = "/media/"

# DJANGO PHONE NUMBER FIELD
PHONENUMBER_DB_FORMAT = "NATIONAL"

PHONENUMBER_DEFAULT_REGION = "NP"

# Cache configuration
CACHES = {
    "default": {
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS" : {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'select2': {
        "BACKEND" : "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS" : {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

# EMAIL_CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("HOST_EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("HOST_PASSWORD")

# File extension rule
ALLOWED_IMAGES_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "JPG", "webp"]
MAX_UPLOAD_IMAGE_SIZE = 2000

LOYALTY_DISCOUNT = 10
DELIVERY_START_PM = 17
DELIVERY_START_AM = 4
DELIVERY_CHARGE = 50
LOYALTY_10_PER_FROM = 10000
LOYALTY_12_PER_FROM = 12000
LOYALTY_13_PER_FROM = 15000
LOYALTY_15_PER_FROM = 20000
