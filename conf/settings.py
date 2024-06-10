import os
from typing import Any, Dict

import environ
import sentry_sdk
from django_log_formatter_asim import ASIMFormatter
from health_check.backends import BaseHealthCheckBackend
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env()
for env_file in env.list('ENV_FILES', default=[]):
    env.read_env(f'conf/env/{env_file}')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# As app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'revproxy',
    'core',
    'directory_healthcheck',
    'health_check.db',
    'health_check.cache',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'core.middleware.PrefixUrlMiddleware',
]

ROOT_URLCONF = 'conf.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]


WSGI_APPLICATION = 'conf.wsgi.application'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# Logging for development
if DEBUG:
    LOGGING: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
        'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler'}},
        'loggers': {
            'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': True},
            '': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        },
    }
else:
    LOGGING: Dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            "asim_formatter": {
                "()": ASIMFormatter,
            },
            "simple": {
                "style": "{",
                "format": "{asctime} {levelname} {message}",
            },
        },
        'handlers': {
            "asim": {
                "class": "logging.StreamHandler",
                "formatter": "asim_formatter",
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        'loggers': {
            "django": {
                "handlers": ["asim"],
                "level": "INFO",
                "propagate": False,
            },
            'sentry_sdk': {'level': 'ERROR', 'handlers': ['asim'], 'propagate': False},
        },
    }

# Sentry
if env.str('SENTRY_DSN', ''):
    sentry_sdk.init(
        dsn=env.str('SENTRY_DSN'), environment=env.str('SENTRY_ENVIRONMENT'), integrations=[DjangoIntegration()]
    )


SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', 16070400)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SSO_UPSTREAM = env.str('SSO_UPSTREAM').rstrip('/')

# test facilitation
TEST_IP_RESTRICTOR_SKIP_SENDER_ID = env.str('TEST_IP_RESTRICTOR_SKIP_SENDER_ID', '')
TEST_IP_RESTRICTOR_SKIP_SENDER_SECRET = env.str('TEST_IP_RESTRICTOR_SKIP_SENDER_SECRET', '')
TEST_SSO_HEALTHCHECK_TOKEN = env.str('TEST_SSO_HEALTHCHECK_TOKEN', '')

SSO_SIGNATURE_SECRET = env.str('SSO_SIGNATURE_SECRET')

FEATURE_URL_PREFIX_ENABLED = True
URL_PREFIX_DOMAIN = env.str('URL_PREFIX_DOMAIN', '')

# health check
DIRECTORY_HEALTHCHECK_TOKEN = 'fsfsdfs'  # env.str('HEALTH_CHECK_TOKEN')
DIRECTORY_HEALTHCHECK_BACKENDS = [
    # health_check.db.backends.DatabaseBackend and
    # health_check.cache.CacheBackend are also registered in
    # INSTALLED_APPS's health_check.db and health_check.cache
    BaseHealthCheckBackend,
]
