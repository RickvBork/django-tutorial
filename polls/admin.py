from django.contrib import admin

# Register your models here.
from .models import Question, Choice


class ChoiceModelAdmin(admin.ModelAdmin):
    """
    Custom admin view sub-class based on the django class ModelAdmin.
    Adds extra information columns to the admin list for Questions.
    Now the associated questions and ids are also displayed per question.
    """
    list_display = ('__str__', 'question', 'id')


class QuestionModelAdmin(admin.ModelAdmin):
    """
    Adds extra information columns to the admin list for Choices.
    Now the associated choices are also displayed per question.
    """
    list_display = ('__str__', 'grab_choice_set', 'id')

    """
    Grabs the choice set for the questions and forces it into a list.
    """
    @staticmethod
    def grab_choice_set(question):
        return list(question.choice_set.all())


# Adds functionality to the admin site for the Choice and Question models.
admin.site.register(Choice, ChoiceModelAdmin)
admin.site.register(Question, QuestionModelAdmin)