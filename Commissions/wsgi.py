"""
WSGI config for Commissions project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/commissions.kaitofletcher.com/web/Commissions')
# print(sys.path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Commissions.settings")


application = get_wsgi_application()
