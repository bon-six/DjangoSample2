from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Question, Choice, Vote
from .apps import QuestionappConfig



class HomepageView (ListView):
    model = Question
    template_name = QuestionappConfig.name+'/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        context['question_list'] = Question.objects.all()
        return context

class QuestionDetailView (DetailView):
    model = Question
    template_name = QuestionappConfig.name+'/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context

'''
def homepage_view(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, QuestionappConfig.name+'/home.html', context)
'''