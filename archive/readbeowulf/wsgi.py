import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "readbeowulf.settings")

application = get_wsgi_application()

# from whitenoise.django import DjangoWhiteNoise  # noqa
#
# application = DjangoWhiteNoise(get_wsgi_application())
