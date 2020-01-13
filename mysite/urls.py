"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import include, path

# When somebody requests a page from the site django will load this list
# ROOT_URLCONF in mysite.settings should point to this list in DOT format
# After finding a match, django will strip the leading 'polls/' string
# The remainder is sent to polls.urls’ URLconf for further processing
urlpatterns = [
    # e.g. /polls/9/vote/ will send 9/vote/ to polls.urls' URLconf
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
