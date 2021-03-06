"""
Django settings for RATS_application project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import datetime
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import configparser
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# RATS_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/backend'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y9)j7ftq*#70$teyq194*!zg%ta%^uet4*(5(s=t&1@3z8uhsa'

CORS_ORIGIN_WHITELIST = (
    'http://0.0.0.0:6004',
    'http://127.0.0.1:6004',
    'http://localhost:3000',
    'http://127.0.0.1:8000',
    'http://34.71.187.210:8000'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', 'http://127.0.0.1:8000', 'http://34.71.187.210', 'localhost', '127.0.0.1']
# config file.
RATS_CONFIG_FILE_PATH = os.path.join(BASE_DIR,
                                     'backend/apps/RATS.conf')
# if not os.path.exists(RATS_CONFIG_FILE_PATH):
#     raise ImproperlyConfigured("Failed to locate configuration file. Expected "
#                                "path: {}".format(RATS_CONFIG_FILE_PATH))
CONFIG = configparser.ConfigParser(allow_no_value=True)
CONFIG.read(RATS_CONFIG_FILE_PATH)

# BASE_URL = CONFIG['settings']['base_url']
# BASE_URL_SERVICES = CONFIG['settings']['base_url_services']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "django_extensions",
    'corsheaders',

    # Apps
    'backend.apps.authentication',
    'backend.apps.home',
    'backend.apps.quant_connect',
    'backend.apps.oauth2',
    'backend.apps.cred',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.apps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'public'),)

WSGI_APPLICATION = 'backend.apps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': CONFIG['database']['name'],
        'USER': CONFIG['database']['user'],
        'PASSWORD': CONFIG['database']['password'],
        'HOST': CONFIG['database']['host'],
        'PORT': CONFIG['database']['port']
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = "authentication.User"


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


REACT_APP_DIR = os.path.join(BASE_DIR, 'frontend')

STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, 'build', 'static'),
]


SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# SECURE_SSL_REDIRECT = False


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.AllowAny",
        "rest_framework.permissions.IsAuthenticated",
        # "rest_framework.permissions.IsAdminUser",
    ],
    # django jwt framework
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",      
    ),
}

# Jwt Authentication
JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}
