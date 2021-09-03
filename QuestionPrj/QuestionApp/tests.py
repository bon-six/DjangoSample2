from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Question, Choice, Vote

# Create your tests here.
class QuestionAppTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
        )
        self.admin = get_user_model().objects.create_superuser(
            username='testadmin',
            email='testadmin@email.com',
            password='secret',
        )
        self.question = Question.objects.create(
            question_text="Your location?",
            pub_date=timezone.now()-timedelta(days=1),
        )
        self.choice = Choice.objects.create(
            choice_text="KL",
            question = self.question,
        )
    
    def test_model_question_string(self):
        question = Question(question_text="Sample Question",pub_date=timezone.now())
        self.assertEqual(str(question),question.question_text)

    def test_model_choice_string(self):
        choice = Choice(choice_text="Sample Options",question=self.question)
        self.assertEqual(str(choice),choice.choice_text)

    def test_model_vote_string(self):
        vote = Vote(voter_name="Guest",vote_date=timezone.now(),choice=self.choice)
        self.assertIn('Guest',str(vote))

    def test_admin_login(self):
        response=self.client.login(username='testadmin',password='secret')
        self.assertTrue(response)
    
    def test_user_login(self):
        response=self.client.login(username='testuser',password='secret')
        self.assertTrue(response)

    def test_home_view(self):
        response=self.client.get(reverse('QuestionApp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your location?')
        self.assertTemplateUsed(response, 'QuestionApp/home.html')

    def test_detail_view(self):
        response=self.client.get(reverse('QuestionApp:question_detail',args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your location?')
        self.assertTemplateUsed(response, 'QuestionApp/detail.html')

    def test_detail_view_no_item(self):
        response=self.client.get(reverse('QuestionApp:question_detail',args=[2]))
        self.assertEqual(response.status_code, 404)

    def test_default_url(self):
        response=self.client.get(reverse('QuestionApp:default'))
        self.assertEqual(response.status_code, 200)
        response=self.client.get('/index.html')
        self.assertEqual(response.status_code, 200)

    def test_invalid_url(self):
        response=self.client.get('/home.html')
        self.assertEqual(response.status_code, 404)
        response=self.client.get('/default.html')
        self.assertEqual(response.status_code, 404)

    #def test_invalid_url2(self):
    #    response=self.client.get('//index.html')
    #    self.assertEqual(response.status_code, 404)
