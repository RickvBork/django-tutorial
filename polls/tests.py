import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice

def create_no_vote_choice_for_a_question(question, choice_text):
    """
    Adds a choice with 0 votes to a question object.
    """

    # Method .create will write to database by calling .save()
    Choice.objects.create(question=question, choice_text=choice_text, votes=0)

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).

    Used in the django test classes below.

    :param days:
    :return Question object:
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# django.test.Testcase subclass
class QuestionModeTests(TestCase):

    """
    The following tests create a Question object and sets the pub_date 30 days in the future
    and subsequently checks if the outcome is False, as expected
    """
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)

        # Question() method will not write to the database.
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """

        # Build the response url for the index view
        response = self.client.get(reverse('polls:index'))

        # Check if the status code corresponds with nominal
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the correct reply.
        self.assertContains(response, "No polls are available.")

        # Check if the latest_question_list is empty
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_without_choices(self):
        """
        If no choice for a question exists, then check if the
        latest_qeustion_list is empty.
        """
        create_question(question_text='This is a question without choices.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page. Choices are added.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_no_vote_choice_for_a_question(question=question, choice_text="This is a choice")

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page. Choices are added.
        """
        question = create_question(question_text="Future question.", days=30)
        create_no_vote_choice_for_a_question(question=question, choice_text='This is a choice for a future question.')

        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed. Choices are added.
        """
        past_question = create_question(question_text="Past question.", days=-30)
        create_no_vote_choice_for_a_question(question=past_question, choice_text='This is a choice for a past question.')

        future_question = create_question(question_text="Future question.", days=30)
        create_no_vote_choice_for_a_question(question=future_question, choice_text='This is a choice for a future question.')

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        Choices are added.
        """
        past_question0 = create_question(question_text="Past question 1.", days=-30)
        create_no_vote_choice_for_a_question(question=past_question0, choice_text='This is a choice for the first old question.')

        past_question1 = create_question(question_text="Past question 2.", days=-5)
        create_no_vote_choice_for_a_question(question=past_question1, choice_text='This is a choice for the second old question.')

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


# Tests for users guessing urls for the detail view
class QuestionDetailViewTests(TestCase):
    """
    Tests for the detailview where questions with their choices are displayed.
    """

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        # Check if the site reponds with a 404 status code
        self.assertEqual(response.status_code, 404)


# Tests for users guessing urls for the results view
class QuestionResultsViewTests(TestCase):
    """
    Tests for the results view where questions are displayed
    with the amount of votes per question.
    """

    def test_past_question(self):
        """
        The results view of a question with a pub_date in the past
        displays the amount of votes per choice.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """
        The results view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)

        # Check if the site reponds with a 404 status code
        self.assertEqual(response.status_code, 404)


# Tests for users guessing urls for the results view
class QuestionVoteViewTests(TestCase):
    """
    Tests for the vote view where questions are displayed
    with the choices and a radio button to select a choice.
    """

    def test_past_question_without_choice(self):
        """
        The vote view of a question with a pub_date in the past
        displays the amount of votes per choice.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:vote', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_with_choice(self):
        """
        The vote view of a question with a pub_date in the past
        displays the amount of votes per choice.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        create_no_vote_choice_for_a_question(question=past_question, choice_text='This is a choice for a past question.')
        url = reverse('polls:vote', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_past_question_with_multiple_choices(self):
        """
        The vote view of a question with a pub_date in the past
        displays the amount of votes per choice.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        create_no_vote_choice_for_a_question(question=past_question, choice_text='Test_1')
        create_no_vote_choice_for_a_question(question=past_question, choice_text='Test2')

        url = reverse('polls:vote', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_future_question(self):
        """
        The vote view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:vote', args=(future_question.id,))
        response = self.client.get(url)

        # Check if the site reponds with a 404 status code
        self.assertEqual(response.status_code, 404)