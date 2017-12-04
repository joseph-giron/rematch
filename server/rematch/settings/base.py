"""
Django settings for rematch project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


# SECRET_KEY must be kept secret, so it is not included in the repository for
# production servers and instead auto-generated and saved to disk on first run
SECRET_KEY_PATH = os.path.join(BASE_DIR, '.rematch_secret.key')
if not os.path.isfile(SECRET_KEY_PATH):
  fd = os.open(SECRET_KEY_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
  try:
    with os.fdopen(fd, 'w') as fh:
      import django.core.management.utils
      fh.write(django.core.management.utils.get_random_secret_key())
  except Exception:
    os.unlink(SECRET_KEY_PATH)
    raise

with open(SECRET_KEY_PATH, 'r') as fh:
  SECRET_KEY = fh.read()
assert len(SECRET_KEY) > 20


# As of django 1.10, allowed hosts are validated in debug as well,
# this disables that and makes sure all hosts are acceptible when
# running in debug mode. for more details see
# https://docs.djangoproject.com/en/1.10/ref/settings/
# for security implications see
# https://docs.djangoproject.com/en/1.10/topics/security/#host-headers-virtual-hosting
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'accounts',
    'collab',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# Backwards compat. with django 1.11
MIDDLEWARE_CLASSES = MIDDLEWARE

ROOT_URLCONF = 'rematch.urls'

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

WSGI_APPLICATION = 'rematch.wsgi.application'


# Django rest framework configuration
REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
  ),

  'DEFAULT_FILTER_BACKENDS': (
    'django_filters.rest_framework.DjangoFilterBackend',
  ),

  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

REST_SESSION_LOGIN = False

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rematch',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES';",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


# Celery configuration
# use django's database to keep celery state
result_backend = 'database'

# only fetch one task per execution slot at a time, let multiple workers behave
worker_prefetch_multiplier = 1

# since most tasks are long and require a lot of memory it is possible to kill
# worker childs after a small amount of tasks and doing so may mitigate any
# object leaks
worker_max_tasks_per_child = 100
