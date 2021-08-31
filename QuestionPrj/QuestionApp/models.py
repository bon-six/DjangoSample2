from django.db import models
import datetime

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

class Votes(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=50)
    vote_date = models.DateTimeField('date voted')
    class Meta:
        verbose_name_plural = "Votes"
    def __str__(self):
        return self.voter_name+' at: '+datetime.datetime.strftime(self.vote_date, "%d %B %Y")




        
    