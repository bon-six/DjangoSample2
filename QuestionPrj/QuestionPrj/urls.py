"""QuestionPrj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Festival Questionnaire admin'
admin.site.site_title = 'Festival Questionnaire'
admin.site.site_url = 'http://localhost:8000/'
admin.site.index_title = 'Festival Questionnaire administration'
admin.empty_value_display = '**Empty**'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/',include('user.urls')),
    path('accounts', include('django.contrib.auth.urls')),
    path('',include('QuestionApp.urls')),
]
