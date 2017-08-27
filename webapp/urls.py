from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^user/(?P<owner_id>[-\w]+)/accounts/$', views.AccountView.as_view()),
    url(r'^prediction/pid/(?P<pk>[-\w]+)/$', views.PredictionRetrieveById.as_view()),
    url(r'^prediction/list/$', views.PredictionRetrieveAll.as_view()),
    url(r'^prediction/$', views.PredictionUpdate.as_view()),
    url(r'^prediction/pid/(?P<pid>[-\w]+)/opt/$', views.PredictionOptionListViews.as_view()),
    url(r'^opt/(?P<oid>[-\w]+)/position$', views.PredictionPositionViews.as_view()),
    url(r'^prediction/admin/validate/(?P<id>[-\w]+)', views.PredictionValidateAdminView.as_view(),
        name='validate_prediction'),
    url(r'^top/$', views.TopAccountViews.as_view()),
]
