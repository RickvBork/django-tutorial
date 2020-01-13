from django.contrib import admin

# Register your models here.
from .models import Question, Choice

"""
Handles the way choices are displayed in the change Question admin.
"""
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


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
    list_display = ('__str__', 'choices', 'pub_date', 'was_published_recently', 'id')

    # Sets the amount of items that can be viewed per page
    list_per_page = 10

    # Allows filtering by publication date
    list_filter = ['pub_date']

    # Allows the admin to search by typing
    search_fields = ['question_text']

    # Force pub_date fields above the question_text field in: http://127.0.0.1:8000/admin/polls/question/'#id'/change/
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],
                              'classes': ['collapse']}),
        ]

    # Add choices to the question change admin
    inlines = [ChoiceInline]

    """
    Grabs the choice set for the questions and forces it into a list.
    """
    @staticmethod
    def choices(question):
        return list(question.choice_set.all())


# Adds functionality to the admin site for the Choice and Question models.
admin.site.register(Choice, ChoiceModelAdmin)
admin.site.register(Question, QuestionModelAdmin)