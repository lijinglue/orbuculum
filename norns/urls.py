from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^norns/player/pid/(?P<pk>[-\w]+)/$', views.PlayerView.as_view()),
    url(r'^norns/dialogue/(?P<pk>[-\w]+)/$', views.DialogueView.as_view()),
]