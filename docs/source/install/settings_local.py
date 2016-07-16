# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
import os

# Generate a secret key
try:
    from secret_key import *
except ImportError:
    from helper_functions.secret_key_generator import *
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
    generate_secret_key(os.path.join(SETTINGS_DIR, 'secret_key.py'))
    from secret_key import *

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Ajuste o caminho para static
STATIC_ROOT = '/var/lib/sistema-nira/nira/static/'

INSTALLED_APPS = (
    #'suit',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cities_light',
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

CEPID_NAME = 'Seu Cepid'

# Aqui você deve colocar as suas configurações de banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'seu_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
    }
}

# Esse trecho só é necessário se o Django Suit for usado
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
        {'label': _('Reports'), 'icon': 'icon-th', 'permissions': 'custom_auth.view_reports', 'models': (
            {'label': _('Academic works'), 'url': '/research/academic_works'},
            {'label': _('Articles'), 'url': '/research/articles'},
            {'label': _('Disseminations'), 'url': '/dissemination/dissemination_report'},
            {'label': _('Meetings'), 'url': '/activity/meetings'},
            {'label': _('Scientific missions'), 'url': '/scientific_mission/report'},
            {'label': _('Seminars'), 'url': '/activity/seminars'},
            {'label': _('Training programs'), 'url': '/activity/training_programs'},
        )},
        {'label': _('Add content'), 'icon': 'icon-upload', 'permissions': 'custom_auth.add_content', 'models': (
            {'label': _('Create/Update citation name'), 'url': '/person/citation_names'},
            {'label': _('Import papers'), 'url': '/research/import_papers'},
        )},
        {'label': _('Documents'), 'icon': 'icon-list-alt', 'permissions': 'custom_auth.create_documents', 'models': (
            {'label': _('FAPESP - appendix 5'), 'url': '/scientific_mission/anexo5/'},
            {'label': _('Seminar poster'), 'url': '/activity/seminar_poster'},
        )},
        '-',
        {'app': 'cities_light', 'icon': 'icon-globe', 'label': _('Cities')},
        {'app': 'custom_auth', 'icon': 'icon-lock', 'label': _('Users')},
        {'app': 'auth', 'icon': 'icon-lock', 'label': _('Groups')},
    ),
}

