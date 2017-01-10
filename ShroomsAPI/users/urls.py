from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.contrib.auth.views import logout

from rest_framework.routers import DefaultRouter

from users.views import RegisterUser

urlpatterns = [
    url(r'^register$', RegisterUser.as_view()),
]

