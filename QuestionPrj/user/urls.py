from django.urls import path, re_path
from .views import MyLoginView

urlpatterns = [
    path('',MyLoginView.as_view(),name='my_login'),
]