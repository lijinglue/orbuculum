from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^player/pid/(?P<pk>[-\w]+)/$', views.PlayerView.as_view()),
    url(r'^dialogue/(?P<pk>[-\w]+)/$', views.DialogueView.as_view()),
    url(r'^story/$', views.StoryView.as_view()),
]