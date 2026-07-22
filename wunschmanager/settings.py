import os
from pathlib import Path
import configparser

BASE_DIR = Path(__file__).resolve().parent.parent

config = configparser.ConfigParser()
config.read(BASE_DIR / 'config.ini')

SECRET_KEY = config.get('django', 'SECRET_KEY')

DEBUG = config.getboolean('django', 'DEBUG')

ALLOWED_HOSTS = config.get('django', 'ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = config.get('django', 'CSRF_TRUSTED_ORIGINS').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wunschliste',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wunschmanager.urls'

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

WSGI_APPLICATION = 'wunschmanager.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'ENGINE'),
        'NAME': BASE_DIR / config.get('database', 'NAME'),
    }
}

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

LANGUAGE_CODE = 'de-de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 3600

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'



PUBLIC_VIEW_PASSWORD = config.get('public_view', 'PASSWORD')
PUBLIC_VIEW_HELP_TEXT = config.get('public_view', 'HELP_TEXT')
CONTACT_EMAIL = config.get('contact', 'EMAIL')
CREATE_WISH_USERNAME = config.get('authentication', 'CREATE_WISH_USERNAME')
CREATE_WISH_PASSWORD = config.get('authentication', 'CREATE_WISH_PASSWORD')
GIFT_HISTORY_USERNAME = config.get('authentication', 'GIFT_HISTORY_USERNAME')
GIFT_HISTORY_PASSWORD = config.get('authentication', 'GIFT_HISTORY_PASSWORD')


