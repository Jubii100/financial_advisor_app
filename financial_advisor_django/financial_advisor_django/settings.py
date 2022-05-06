import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^ka*y#vs4wn%g8&$rzdi&4yltlf7#20=jzgqpv!#x&gd36k$6-'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'behaviors.apps.BehaviorsConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'financial_advisor_django.urls'

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

WSGI_APPLICATION = 'financial_advisor_django.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'financial_advisor',
        'USER': 'postgres',
        'PASSWORD': '4321',
        'HOST': 'localhost',
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
LOGIN_REDIRECT_URL = '/users/user_profile/'
LOGOUT_REDIRECT_URL = '/login/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'loggers': {
        'django': {
            'handlers': ['debug'],
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['requests'],
        },
        'django.db.backends': {
            'handlers': ['db'],
        }
    },
    'handlers': {
        'debug': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './logs/debug.log',
            'formatter': 'formatter_1',
        },
        'requests': {
            'class': 'logging.FileHandler',
            'filename': './logs/requests.log',
            'formatter': 'formatter_2',
        },
        'db': {
            'class': 'logging.FileHandler',
            'filename': './logs/db.log',
            'formatter': 'formatter_3',
        }
    },
    'formatters': {
        'formatter_1': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'formatter_2': {
            'format': '{asctime} {message}',
            'style': '{',
        },
        'formatter_3': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        }
    }
}
