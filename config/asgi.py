"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()

from uvicorn.workers import UvicornWorker


class DjangoUvicornWorker(UvicornWorker):
    """
    Generate UvicornWorker with lifespan='off', because Django does not
    (and probably will not https://code.djangoproject.com/ticket/31508)
    support Lifespan.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.lifespan = "off"
