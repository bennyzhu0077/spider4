"""
WSGI config for spider_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from leancloud import Engine
from leancloud import LeanEngineError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spider_project.settings')

application = Engine(get_wsgi_application())
