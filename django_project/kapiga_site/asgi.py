"""
ASGI config for Dr. Saidi Kapiga Research Site
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapiga_site.settings')

application = get_asgi_application()
