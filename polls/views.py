from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):

    # Default name would be: <app name>/<model name>_list.html
    # polls/question_list.html
    # template_name overwrites this to use previous names used for the existing templates
    template_name = 'polls/index.html'

    # Default name would be: <model name>_list
    # question_list
    # Overwrite with context_object_name to use the same variable name as in the index template
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Returns the last 5 published questions, but omits those
        submitted in the future. The .filter(pub_date__lte=timezone.now())
        returns a set where the pub_date is less than, or equal to (lte) timezone.now().
        It also omits questions that have no choice at all.
        """
        return Question.objects.filter(
            choice__isnull=False).filter(
            pub_date__lte=timezone.now()
        ).distinct().order_by('-pub_date')[:5]

        # return Question.objects.filter(
        #     pub_date__lte=timezone.now()
        # ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question

    # Default name would be: <app name>/<model name>_list.html
    # polls/question_detail.html
    # template_name overwrites this to use previous names used in the existing templates
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Exclude any question that aren't published yet. While future questions don’t appear
        in the index, users can still reach them if they know or guess the right URL.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Exclude any question that aren't published yet. While future questions don’t appear
        in the index, users can still reach them if they know or guess the right URL.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):

    # Filters out future questions, incorrect ids and/or questions without a choice.
    queryset = Question.objects.filter(
            pk=question_id).filter(
            pub_date__lte=timezone.now()).filter(
            choice__isnull=False
        ).distinct().order_by('-pub_date')[:5]

    # If the question doesn't exist, or is in the future, show 404
    question = get_object_or_404(queryset)

    try:
        # Grab the string representing the choice number, and check if it exists
        # request.POST['choice'] returns the id of the selected 'choice' radio.
        # In this case a number as defined in polls/detail.html
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        # Set the context for the respons
        context = {
            'question': question,
            'error_message': 'You didn\'t select a choice.',
        }

        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', context)

    # Save choice count and return a response (Redirect for POST)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))