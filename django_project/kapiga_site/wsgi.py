"""
WSGI config for Dr. Saidi Kapiga Research Site
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapiga_site.settings')

application = get_wsgi_application()
