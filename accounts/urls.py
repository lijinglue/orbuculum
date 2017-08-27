from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^register/$', UserRegistrationService.as_view()),
    url(r'^profile/$', ProfileService.as_view()),
]
