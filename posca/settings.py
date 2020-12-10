"""
Django settings for posca project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


##########
#SECRET_KEY =
##########

# SECURITY WARNING: don't run with debug turned on in production!

################
#DEBUG = True
#####heroku#####
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'igposca',
    'django_celery_results',
    'rest_framework',
]

################
#MIDDLEWARE = [
#    'django.middleware.security.SecurityMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'social_django.middleware.SocialAuthExceptionMiddleware',
#    'django.contrib.sites.middleware.CurrentSiteMiddleware',
#]
#####heroku#####
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
#####heroku#####


ROOT_URLCONF = 'posca.urls'

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
                'social_django.context_processors.backends',  # これを追加
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'posca.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

#####heroku#####
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': '',
        'HOST': 'host',
        'PORT': '',
    }
}
#####heroku#####


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

#####heroku#####
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#####heroku#####


######################################
# Authentication                     #
######################################

# Don't forget this little dude.
SITE_ID = 1
#LOGIN_URL='line_login'
# ログインのリダイレクトURL
#LOGIN_REDIRECT_URL = 'account'

# ログアウトのリダイレクトURL
#ACCOUNT_LOGOUT_REDIRECT_URL = 'index'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ]
}


#SOCIALACCOUNT_PROVIDERS = {
    #'line': {
    #    'AUTH_PARAMS': {'bot_prompt':'aggressive','prompt':'consent'},
    #    'SCOPE': ['profile','openid'],
    #}
    #bot_prompt=normal&prompt=consent'prompt':'consent','redirect_uri':callback_uri
#}


#####heroku#####
try:
    from .local_settings import *
except ImportError:
    pass
#####heroku#####





#####heroku#####
db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)
#####heroku#####

#####heroku#####
if not DEBUG:
    #SECURE_SSL_REDIRECT = True
    #SMARTMAIL=os.environ['smartmail']
    #TECHBEEMAIL=os.environ['techbeeMail']
    #OHTSUKIMAIL=os.environ['ohtsukiMail']
    #MYMAILPASS=os.environ['mymailpass']
    #MYMAIL=os.environ['mymail']
    #YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
    #YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
    SECRET_KEY = os.environ['SECRET_KEY']
    IGKEY=os.environ['IGKEY']
    import django_heroku #追加
    django_heroku.settings(locals()) #追加
    """
    CACHES = {
        "default": {
             "BACKEND": "redis_cache.RedisCache",
             "LOCATION": os.environ.get('HEROKU_REDIS_GRAY_URL'),
        }
    }
    BROKER_URL = os.environ.get("HEROKU_REDIS_GRAY_URL")
    CELERY_RESULT_BACKEND = os.environ.get("HEROKU_REDIS_GRAY_URL")
    """


#####heroku#####


IGKEY='poscagram_key'
AUTH_USER_MODEL = 'igposca.MyUser'


###### django-celery configuations ######
from djcelery import setup_loader
setup_loader()
# Tasks will be executed asynchronously.
"""
CELERY_ALWAYS_EAGER = False
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60


#BROKER_URL = 'redis://localhost'
#CELERY_RESULT_BACKEND = 'redis'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

"""
if not DEBUG:
    from datetime import timedelta
    from celery.schedules import crontab
    CELERY_BEAT_SCHEDULE = {
        'task-number-one': {
            'task': 'task_search_taged',
            'schedule': crontab(minute=0, hour=12),
        },
        """
        'task-likes': {
            'task': 'task_likes',
            'schedule': timedelta(minutes=60),
        },
        """

    }
    #'args': (10, 15),
    #'schedule': timedelta(minutes=24*60),
    #'schedule': crontab(minute=30, hour=21),
    CELERY_ALWAYS_EAGER = False
    CELERY_BROKER_URL = os.environ.get('HEROKU_REDIS_GRAY_URL')
    CELERY_RESULT_BACKEND = os.environ.get('HEROKU_REDIS_GRAY_URL')
    CELERY_BROKER_HOST = os.environ.get('DATABASE_URL')
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Asia/Tokyo'
    CELERY_TASK_TRACK_STARTED = True # taskが開始状態になったことを確認できるための設定（後述）

    import ssl

    BROKER_USE_SSL = {'ssl_cert_reqs': 'none'}
    CELERY_REDIS_BACKEND_USE_SSL = {'ssl_cert_reqs': ssl.CERT_NONE}

#celery -A posca worker -l INFO
#celery -A posca worker --concurrency=1
#worker: celery -A posca worker -B -l info

BROKER_URL = 'redis://localhost'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
