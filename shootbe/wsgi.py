from django.core.wsgi import get_wsgi_application

import os

os.environ["DJANGO_SETTINGS_MODULE"] = "shootbe.settings"

application = get_wsgi_application()
