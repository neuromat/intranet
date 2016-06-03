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

AUTH_USER_MODEL = 'custom_auth.User'

# Application definition

INSTALLED_APPS = (
    'suit',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cep',
    'django_jenkins',
    'cities_light',
)

# Possible tasks for Jenkins

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_sloccount',
    'django_jenkins.tasks.run_pylint',
)

PROJECT_APPS = (
    'custom_auth',
    'person',
    'activity',
    'dissemination',
    'research',
    'scientific_mission',
)

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
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

SUIT_CONFIG = {
    'ADMIN_NAME': 'NIRA',
    'MENU_OPEN_FIRST_CHILD': False,
    'HEADER_DATE_FORMAT': 'l, d F Y',
    'MENU': (
        {'app': 'activity', 'icon': 'icon-calendar'},
        {'app': 'dissemination', 'icon': 'icon-facetime-video'},
        {'app': 'person', 'icon': 'icon-user'},
        {'app': 'research', 'icon': 'icon-book'},
        {'app': 'scientific_mission', 'icon': 'icon-plane'},
        {'label': 'Reports', 'icon': 'icon-th', 'permissions': 'user.is_nira_admin', 'models': (
            {'label': 'Academic works', 'url': '/research/academic_works'},
            {'label': 'Articles', 'url': '/research/articles'},
            # {'label': 'Books and chapters', 'url': ''},
            {'label': 'Disseminations', 'url': '/dissemination/dissemination_report'},
            {'label': 'Meetings', 'url': '/activity/meetings'},
            {'label': 'Scientific missions', 'url': '/scientific_mission/report'},
            {'label': 'Seminars', 'url': '/activity/seminars'},
            {'label': 'Training programs', 'url': '/activity/training_programs'},
        )},
        {'label': 'Add content', 'icon': 'icon-upload', 'permissions': 'user.is_nira_admin', 'models': (
            {'label': 'Create/Update citation name', 'url': '/person/citation_names'},
            {'label': 'Import papers', 'url': '/research/import_papers'},
        )},
        {'label': 'Documents', 'icon': 'icon-list-alt', 'permissions': 'user.is_nira_admin', 'models': (
            # {'label': 'FAPESP - appendix 5', 'url': ''},
            {'label': 'Seminar poster', 'url': '/activity/seminar_poster'},
        )},
        '-',
        {'app': 'cities_light', 'icon': 'icon-globe', 'label': 'Cities'},
        {'app': 'custom_auth', 'icon': 'icon-lock', 'label': 'Users'},
        {'app': 'auth', 'icon': 'icon-lock', 'label': 'Groups'},
    ),
}

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
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = '/login/'

try:
    from settings_local import *
except ImportError:
    pass
