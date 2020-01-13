# Note: import datetime and from django.utils import timezone
# Done to reference Python’s standard datetime module and Django’s time-zone-related utilities in django.utils.timezone respectively.
import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # Adds a recognizable object name for its representation
    def __str__(self):
        return self.question_text

    # Returns True or False depending on if the question was asked within a
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # Adds a recognizable object name for its representation
    def __str__(self):
        return self.choice_text