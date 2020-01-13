from django.urls import path
from . import views

# Differentiates between apps within a project
app_name = 'polls'

# Determines how the urls are structured
# To get from a URL to a view, Django uses what are known as ‘URLconfs’.
# A URLconf maps URL patterns to views.
# The 'name' values as called by the {% url %} template tag in the template html files
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/specifics/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]