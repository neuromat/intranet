"""
WSGI config for NIRA project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

# Altere o path de acordo com seu sistema
# aqui usamos o caminho /var/lib/sistema-nira/nira
paths = ['/var/lib', '/var/lib/sistema-nira', '/var/lib/sistema-nira/nira',]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
