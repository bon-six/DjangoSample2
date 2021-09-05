from django.http.response import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Question, Choice, Vote, Comment
from .apps import QuestionappConfig

class HomepageView (ListView):
    model = Question
    template_name = QuestionappConfig.name+'/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        context['question_list'] = Question.objects.all()
        context['comment_list'] = Comment.objects.all()
        return context

class QuestionDetailView (DetailView):
    model = Question
    template_name = QuestionappConfig.name+'/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context

class VoteResultView (DetailView):
    model = Question
    template_name = QuestionappConfig.name+'/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context

class CommentDetailView (DetailView):
    model = Comment
    template_name = QuestionappConfig.name+'/view_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context

class CommentAddView (CreateView):
    model = Comment
    template_name = QuestionappConfig.name+'/new_comment.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context

class CommentUpdateView (UpdateView):
    model = Comment
    template_name = QuestionappConfig.name+'/new_comment.html'
    fields = ['comment_title', 'comment_content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context

class CommentDeleteView (DeleteView):
    model = Comment
    template_name = QuestionappConfig.name+'/delete_comment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context
    
    def get_success_url(self):
        return reverse_lazy(QuestionappConfig.name+':home')
'''
def homepage_view(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, QuestionappConfig.name+'/home.html', context)
'''