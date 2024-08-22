from django.urls import path

from .views import index,SignUp,HomeView,chat_room

urlpatterns=[
    path('realchat/',index,name='realchat'),
    path('signup/',SignUp.as_view(),name='signup'),
    path('',HomeView.as_view(),name='home'),
    path('chat/<str:room_name>/', chat_room, name='chat'),
    
]