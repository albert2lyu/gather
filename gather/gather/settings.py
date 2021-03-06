#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Django settings for gather project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

LOGIN_URL = '/account/login/'
WASH_MURL = '/wash/manage/'
WASH_URL = '/wash/regist/'

ADMINS = (
    ('zhangbo', '413761980@qq.com'),
)
# Application definition

INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'gather',
    'config',
    'bookmark',
    'common',
    'help',
    'share',
    'comment',
    'chatting',
    'wash',
    'wechat',
    'djcelery',
    # 'debug_toolbar',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.ClickLogMiddleWare',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "common.context_processors.basket",
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
)

ROOT_URLCONF = 'gather.urls'

WSGI_APPLICATION = 'gather.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Chongqing'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = os.path.join(os.path.join(BASE_DIR, ".."), 'static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, os.path.join(os.pardir, "media"))

MEDIA_URL = "/media/"

# logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        # 'special': {
        #     '()': 'project.logging.SpecialFilter',
        #     'foo': 'bar',
        # }
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/gather_debug.log'),
            'formatter': 'verbose',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/gather_info.log'),
            'formatter': 'verbose',
        },
        'err': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/gather_err.log'),
            'formatter': 'verbose',
        },
        'statistics': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/statistics.log'),
            'formatter': 'verbose',
        },
        'click': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/click.log'),
            'formatter': 'verbose',
        },
        'login': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/login.log'),
            'formatter': 'verbose',
        },
        
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'gather': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            # 'filters': ['special']
        },
        'debug': {
            'handlers': ['debug'],
            'level': 'DEBUG',
        },
        'info': {
            'handlers': ['info'],
            'level': 'INFO',
        },
        'err': {
            'handlers': ['err'],
            'level': 'ERROR',
        },
        'statistics': {
            'handlers': ['statistics'],
            'level': 'INFO',
        },
        'click': {
            'handlers': ['click'],
            'level': 'INFO',
        },
        'login': {
            'handlers': ['login'],
            'level': 'INFO',
        },
    }
}

SESSION_ENGINE = 'utils.session_backend'

# admin页面时间格式
DATETIME_FORMAT = 'Y-m-d'

SESSION_COOKIE_AGE = 60 * 60 * 2
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# django-celery
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
BROKER_URL = 'redis://localhost:6379/0'
CELERY_DISABLE_RATE_LIMITS = True
# celery worker --app=project.celery:app --loglevel=INFO

# 验证码过期时间 2分钟
VERIFY_CODE_EXPIRE = 120

try:
    from local_settings import *
except ImportError:
    pass

# xieshanshishadiao

