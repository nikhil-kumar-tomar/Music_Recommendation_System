"""
Django settings for music_app project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
import redis
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY",default="p83@s1-#+!3vg9dxm99&gndey*(v#*yvv5kqa^&*1#h%lm#cgw")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*'] # Requires IP address of production server as an addition as well
CORS_ALLOWED_ORIGINS=["http://*"]
CSRF_TRUSTED_ORIGINS = ['http://*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'music_platform',
    'api',
    # Third party below
    'django_browser_reload',
    'widget_tweaks',
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'music_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'music_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':config("DATABASE_db",default="music"),
        'USER': config("DATABASE_USER",default="postgres"),
        'PASSWORD': config("DATABASE_PASSWORD",default="123456789"),
        'HOST': config("Database_HOST",default="127.0.0.1"),
        'PORT': config("Database_PORT",default="5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{config('CACHE_URL')}",
    }
}

REDIS_POOL = redis.ConnectionPool.from_url(f'{CACHES["default"]["LOCATION"]}/0')
REDIS_CONNECTION = redis.Redis(connection_pool=REDIS_POOL)


CELERY_BROKER_URL = f"{config('CELERY_BROKER_URL')}"
CELERY_RESULT_BACKEND = f"{config('CELERY_RESULT_BACKEND')}"
CACHE_PREFIX_USER = f"{config('CACHE_PREFIX_USER')}"
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config("TIME_ZONE",default='Asia/Kolkata') 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL="music_platform.custom_user"
AUTHENTICATION_BACKENDS=['music_platform.backends.email_backend']

# ML SERVICE 
ML_SERVICE = config("ML_SERVICE","http://127.0.0.1:2001")
NUMBER_OF_SONGS_PER_ARTIST = config("NUMBER_OF_SONGS_PER_ARTIST")
NUMBER_OF_ARTISTS = config("NUMBER_OF_ARTISTS")
# SPOTIFY
SPOTIFY_ID=config("SPOTIFY_ID")
SPOTIFY_SECRET=config("SPOTIFY_SECRET")
