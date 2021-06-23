import datetime

from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.core.urlresolvers import reverse

def create_question(question_text, days):
	#creates a question with the given question_text published the 
	#given number of days offset to now, (0 is today, -1 is yesterday, 1 is tomorrow, etc.)
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		future_question = create_question(question_text='Future question.', days=5)
		response = self.client.get(reverse('polls:detail',args=(future_question.id,)))
		self.assertEqual(response.status_code,404)

	def test_detail_view_with_a_past_question(self):
		past_question = create_question(question_text='Past question.', days=-5)
		response = self.client.get(reverse('polls:detail',args=(past_question.id,)))
		self.assertContains(response, past_question.question_text, status_code=200)



class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_index_view_with_a_past_questions(self):
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

	def test_index_view_with_a_future_questions(self):
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available", status_code=200)
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_index_view_with_future_and_past_question(self):
		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

	def test_index_view_with_two_past_questions(self):
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 2.>', '<Question: Past question 1.>'])


class QuestionMethodTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		#was_published_recently() should return False for questions whose
		#pub_date is in the future.

		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		#was_published_recently() should return False for questions whose
		#pub_date is more than one day old

		time = timezone.now() - datetime.timedelta(days=45)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		#was_published_recently() should return True for questions whose
		#pub_date is one day old, or more recently

		time = timezone.now() - datetime.timedelta(hours=2)
		future_question = Question(pub_date=time)
		self.assertEqual(future_question.was_published_recently(), True)
