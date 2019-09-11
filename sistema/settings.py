# -*- coding: utf-8 -*-
"""
Django settings for sistema project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost']

SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

AUTH_USER_MODEL = 'custom_auth.User'

# Application definition

INSTALLED_APPS = (
    'modeltranslation',
    'suit',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cities_light',
    'solo',
    'django_cleanup',
)

PROJECT_APPS = (
    'configuration',
    'custom_auth',
    'person',
    'activity',
    'dissemination',
    'research',
    'scientific_mission',
)

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sistema.urls'

WSGI_APPLICATION = 'sistema.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
    }
}

# Fixtures

FIXTURE_DIRS = (
    '/person/fixtures/',
    'research/fixtures/',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

# default language
LANGUAGE_CODE = 'en'

# list of activated languages
LANGUAGES = (
    ('pt-br', u'Português'),
    ('en', u'English'),
)

# enable django’s translation system
USE_I18N = True

# specify path for translation files
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en', 'pt', 'abbr']

TIME_ZONE = 'America/Sao_Paulo'

USE_L10N = True

USE_TZ = True

DECIMAL_SEPARATOR = ','

USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = ''
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = '/login/'

CEPID_NAME = 'Example CEPID Name'

from django.utils.translation import ugettext_lazy as _
SUIT_CONFIG = {
    'ADMIN_NAME': 'NIRA',
    'MENU_OPEN_FIRST_CHILD': False,
    'HEADER_DATE_FORMAT': 'l, d F Y',
    'MENU': (
        {'app': 'configuration', 'icon': 'icon-cog'},
        {'app': 'activity', 'icon': 'icon-calendar'},
        {'app': 'dissemination', 'icon': 'icon-facetime-video'},
        {'app': 'person', 'icon': 'icon-user'},
        {'app': 'research', 'icon': 'icon-book'},
        {'app': 'scientific_mission', 'icon': 'icon-plane'},
        {'label': _('Reports'), 'url': '/reports/',
         'icon': 'icon-th', 'permissions': 'custom_auth.view_reports', 'models': (
            {'label': _('Academic works'), 'url': '/reports/academic_works'},
            {'label': _('Articles'), 'url': '/reports/articles'},
            {'label': _('Disseminations'), 'url': '/reports/dissemination'},
            {'label': _('Meetings'), 'url': '/reports/meetings'},
            {'label': _('Researchers'), 'url': '/reports/researchers'},
            {'label': _('Scientific missions'), 'url': '/reports/scientific_mission'},
            {'label': _('Seminars'), 'url': '/reports/seminars'},
            {'label': _('Training programs'), 'url': '/reports/training_programs'},
        )},
        {'label': _('Add content'), 'url': '/add_content',
         'icon': 'icon-upload', 'permissions': 'custom_auth.add_content', 'models': (
            {'label': _('Create/Update citation name'), 'url': '/add_content/citation_names'},
            {'label': _('Import papers'), 'url': '/add_content/import_papers'},
        )},
        {'label': _('Documents'), 'url': '/documents',
         'icon': 'icon-list-alt', 'permissions': 'custom_auth.create_documents', 'models': (
            {'label': _('Certificate'), 'url': '/documents/certificate'},
            {'label': _('FAPESP - appendix 5'), 'url': '/documents/anexo5'},
            {'label': _('FAPESP - appendix 6'), 'url': '/documents/anexo6'},
            {'label': _('FAPESP - appendix 7'), 'url': '/documents/anexo7'},
            {'label': _('FAPESP - appendix 9'), 'url': '/documents/anexo9'},
            {'label': _('Seminar poster'), 'url': '/documents/seminars_poster'},
        )},
        '-',
        {'app': 'cities_light', 'icon': 'icon-globe', 'label': _('Cities')},
        {'app': 'custom_auth', 'icon': 'icon-lock', 'label': _('Users')},
        {'app': 'auth', 'icon': 'icon-lock', 'label': _('Groups')},
    ),
}

try:
    from .settings_local import *
except ImportError:
    pass
