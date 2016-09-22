# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
import os

# Generate a secret key
try:
    from secret_key import *
except ImportError:
    from helpers.views.secret_key_generator import *
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
    generate_secret_key(os.path.join(SETTINGS_DIR, 'secret_key.py'))
    from secret_key import *

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Ajuste o caminho para static
STATIC_ROOT = '/var/lib/sistema-nira/nira/static/'

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
