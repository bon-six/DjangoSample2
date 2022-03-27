from django.http.response import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from .models import Question, Choice, Vote, Comment
from .apps import QuestionappConfig
from .forms import VotingForm

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

class CommentAddView (LoginRequiredMixin, CreateView):
    model = Comment
    template_name = QuestionappConfig.name+'/new_comment.html'
    fields = ['comment_title','comment_content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        form.instance.comment_date = timezone.now()
        return super().form_valid(form)

class CommentUpdateView (LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = QuestionappConfig.name+'/new_comment.html'
    fields = ['comment_title', 'comment_content']
    
    def get(self, request, *args, **kwargs):
        if (not request.user) or (str(request.user) != self.get_object().user_name):
            raise PermissionDenied
        return super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context

class CommentDeleteView (LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = QuestionappConfig.name+'/delete_comment.html'

    def get(self, request, *args, **kwargs):
        if (not request.user) or (str(request.user) != self.get_object().user_name):
            raise PermissionDenied
        return super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = QuestionappConfig.name
        return context
    
    def get_success_url(self):
        return reverse_lazy(QuestionappConfig.name+':home')

def check_user_in_answered_db(user_name):
    voted_set = Vote.objects.filter(voter_name=user_name)
    context={}
    if voted_set:
        context['error_msg'] = 'You already finished questionnaire!'
        context['voted_set'] = voted_set
        context['user'] = user_name
    return context

def check_user_answered_all(request):
    context={}
    if (answered:=request.session.get('answered')) != None and \
              len(answered) == len(Question.objects.all()):
        voting_set = []
        for question_id, choice_id in answered:
            question =  get_object_or_404(Question, pk=question_id)
            choice = get_object_or_404(Choice, pk=choice_id)
            voting_set.append((question, choice))
        context['voting_set'] = voting_set
        context['user'] = str(request.user)
    return context

class VotingStartView(LoginRequiredMixin,View):
    def get(self, request):
        user_name = str(request.user)
        if check_user_in_answered_db(user_name) != {} or check_user_answered_all(request) != {}:
            return redirect(reverse(QuestionappConfig.name+':voted'))
        else:
            answered_count = 0
            if (answered := request.session.get('answered')) != None:
                answered_count = len(answered)
            return redirect(reverse(QuestionappConfig.name+':voting', args=(answered_count+1,)))
'''
def get_user_name(request):
    context = {'app_name': QuestionappConfig.name}
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            if request.POST:
                if (user_name:=request.POST.get('user_name')) != None and (user_name:=user_name.strip()) != '':
                    # got a user_name. start from question No.1 if db has no recor. if has record already done
                    request.session['user_name'] = user_name
                    if check_user_in_db(user_name) != {}:
                        return redirect(reverse(QuestionappConfig.name+':voted'))
                    else:
                        return redirect(reverse(QuestionappConfig.name+':voting', args=(1,)))
            context['error_msg'] = 'You did not key in a correct name!'
        else:
            # check test cookie. it not succeed, then prompt user to accpet cookie in browser setting
            context['error_msg'] = 'Please change your browser setting to accept cookie!'
    elif request.method == 'GET':
        if (user_name:=request.session.get('user_name')) != None:
            # need check if already voted for some questions.
            # if not voted, need check session data see how many has already answered and continue from the next
            if check_user_in_db(user_name) != {} or check_user_answered_all(request) != {}:
                return redirect(reverse(QuestionappConfig.name+':voted'))
            else:
                answered_count = 0
                if (answered := request.session.get('answered')) != None:
                    answered_count = len(answered)
                return redirect(reverse(QuestionappConfig.name+':voting', args=(answered_count+1,)))
        else:
            # a new user_name come to vote.
            # need add test cookie, activate session.
            request.session.set_test_cookie()
    # if any error happen, send the same form to user again, possibly with the error_msg added.
    return render(request, QuestionappConfig.name+'/get_user_name.html', context)
'''
class VotingView(LoginRequiredMixin, FormView):
    
    form_class = VotingForm
    template_name = QuestionappConfig.name+'/voting.html'

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = VotingForm(question)
        context = {'app_name': QuestionappConfig.name}
        context['question'] = question
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = VotingForm(question, request.POST)
        if form.is_valid():
            choice_id = int(form.cleaned_data['choice'])
            selected_choice = question.choice_set.all()[choice_id]
            if (answered:=request.session.get('answered')) == None:
                answered = [(pk, selected_choice.pk)]
            else:
                answered.append((pk, selected_choice.pk))
            request.session['answered']=answered
            # finish one question, goes to next question. or if already last one, goes to voted.
            if check_user_answered_all(request) != {}:
                return redirect(reverse(QuestionappConfig.name+':voted'))
            else:
                return redirect(reverse(QuestionappConfig.name+':voting', args=(pk+1,)))
        else:
            context = {'app_name': QuestionappConfig.name}
            context['question'] = question
            context['form'] = form
            context['error_msg'] = 'You did not choose any options!'
            return self.render_to_response(context)
'''
def voting(request, pk):
    context = {'app_name': QuestionappConfig.name}
    question = get_object_or_404(Question, pk=pk)
    context['question'] = question
    if request.method == 'POST':
        if (choice_id := request.POST.get('choice')) != None:
            choice_id = int(choice_id)
            selected_choice = question.choice_set.all()[choice_id-1]
            if (answered:=request.session.get('answered')) == None: 
                answered = [(pk, selected_choice.pk)]
            else:
                answered.append((pk, selected_choice.pk))
            request.session['answered']=answered
            # finish one question, goes to next question. or if already last one, goes to voted.
            if check_user_answered_all(request) != {}:
                return redirect(reverse(QuestionappConfig.name+':voted'))
            else:
                return redirect(reverse(QuestionappConfig.name+':voting', args=(pk+1,)))
        else:
            context['error_msg'] = 'You did not choose any options yet!'
    return render(request, QuestionappConfig.name+'/voting.html', context)
'''
class VotedView(LoginRequiredMixin, TemplateView):
    template_name = QuestionappConfig.name+'/voted.html'

    def get(self, request):
        user_name = str(request.user)
        if (context1:=check_user_in_answered_db(user_name)) == {} and \
            (context1:=check_user_answered_all(request)) == {}:
            raise Http404
        context = {'app_name': QuestionappConfig.name}
        context.update(context1)
        return self.render_to_response(context)

    def post(self, request):
        user_name = str(request.user)
        if (answered:=request.session.get('answered')) == None or len(answered) != len(Question.objects.all()):
            raise Http404
        with transaction.atomic():
            for question_id, choice_id in answered:
                choice = get_object_or_404(Choice, pk=choice_id)
                vote = Vote(choice=choice, voter_name=user_name, vote_date=timezone.now())
                vote.save()
        return redirect(reverse(QuestionappConfig.name+':home'))
'''
def voted(request):
    context = {}
    if (user_name:=request.session.get('user_name')) == None:
        raise Http404
    if request.method == 'GET':
        if (context1 := check_user_in_answered_db(user_name)) != {}:
            context.update(context1)
            return render(request, 'QuesApp/voted.html', context)
        if (context1:=check_user_answered_all(request)) != {}:
            context.update(context1)
            return render(request, 'QuesApp/voted.html', context)
        else:
            raise Http404
    if request.method == 'POST':
        if (context1 := check_user_in_answered_db(user_name)) == {}:
            if (answered:=request.session.get('answered')) != None and \
              len(answered) == len(Question.objects.all()):
                with transaction.atomic():
                    for question_id, choice_id in answered:
                        choice = get_object_or_404(Choice, pk=choice_id)
                        vote = Vote(choice=choice, voter_name=user_name, vote_data=timezone.now())
                        vote.save()
            else:
                raise Http404
        return redirect(reverse('home'))
'''