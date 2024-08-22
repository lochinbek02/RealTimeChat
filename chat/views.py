from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import TemplateView,ListView,CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Message
# Create your views here.
class SignUp(CreateView):
    form_class =UserCreationForm
    
    success_url=reverse_lazy('login')
    template_name='registration/signup.html'
def index(request):
    return render(request, 'index.html',context={'text':'Hello World'})
class HomeView(TemplateView):
  
    template_name='home.html'
def chat_room(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    
    return render(request, 'chat.html', {
        'room_name': room_name,
        'messages': messages
    })