from django.urls import path, re_path
from .consumers import ChatConsumer, ChatConsumerTwo
ws_urlpatterns=[
    path('ws/chat/',ChatConsumer.as_asgi()),
    path('ws/chat/<str:room_name>/', ChatConsumerTwo.as_asgi()),
]