from django.db import models
from django.urls import reverse, reverse_lazy
import datetime

from .apps import QuestionappConfig

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=50)
    vote_date = models.DateTimeField('date voted')
    class Meta:
        verbose_name_plural = "Votes"
    def __str__(self):
        return self.voter_name+': '+datetime.datetime.strftime(self.vote_date, "%d %B %Y")

class Comment(models.Model):
    user_name = models.CharField(max_length=50)
    comment_title = models.CharField(max_length=200)
    comment_content = models.TextField()
    comment_date = models.DateTimeField('date&time')
    def __str__(self):
        return self.comment_title+' by '+self.user_name
    def get_absolute_url(self):
        return reverse_lazy(QuestionappConfig.name+':home')



        
    