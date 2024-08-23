import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realTime.settings')

# Ensure the application is initialized before importing anything else
application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import ws_urlpatterns
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ws_urlpatterns
        )
    ),
})
