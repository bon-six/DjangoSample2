from django.shortcuts import render
from django.contrib.auth.views import LoginView
# Create your views here.

class MyLoginView (LoginView):
    def get_success_url(self):
        if (url:=self.get_redirect_url()):
            return url
        else:
            return super().get_success_url()