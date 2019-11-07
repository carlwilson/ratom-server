"""
WSGI config for ratom_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from ratom_api import load_env

load_env.load_env()
if 'DATABASE_URL' in os.environ:
    # Dokku or similar
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ratom_api.settings.deploy")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ratom_api.settings")

application = get_wsgi_application()

try:
    from whitenoise.django import DjangoWhiteNoise
except ImportError:
    pass
else:
    application = DjangoWhiteNoise(application)
