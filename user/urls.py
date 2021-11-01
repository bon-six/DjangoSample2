from django.urls import path, re_path
from .views import MyLoginView, SignupView

urlpatterns = [
    path('signup',SignupView.as_view(),name='my_signup'),
    path('',MyLoginView.as_view(),name='my_login'),
]