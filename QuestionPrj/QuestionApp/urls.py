from django.urls import path

from .apps import QuestionappConfig
from .views import HomepageView, QuestionDetailView, VoteResultView, \
                   CommentAddView, CommentDetailView, CommentUpdateView, CommentDeleteView

app_name = QuestionappConfig.name
urlpatterns = [
    path('result/<int:pk>/', VoteResultView.as_view(), name='vote_result'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('comment/<int:pk>/del/',CommentDeleteView.as_view(), name='del_comment'),
    path('comment/<int:pk>/edit/',CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/',CommentDetailView.as_view(), name='view_comment'),
    path('comment/',CommentAddView.as_view(), name='add_comment'),
    path('index.html', HomepageView.as_view(), name='default'),
    path('', HomepageView.as_view(), name='home'),
]