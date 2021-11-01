from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
# Create your views here.

class MyLoginView (LoginView):
    def get_success_url(self):
        if (url:=self.get_redirect_url()):
            return url
        else:
            return super().get_success_url()

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('my_login')
    template_name = 'user/signup.html'