from django.urls import path

from .apps import QuestionappConfig
from .views import HomepageView, QuestionDetailView

app_name = QuestionappConfig.name
urlpatterns = [
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('', HomepageView.as_view(), name='home'),
]