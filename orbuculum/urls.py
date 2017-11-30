"""orbuculum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.utils.functional import lazy
from rest_framework_swagger.views import get_swagger_view
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import user_passes_test

from orbuculum import settings

schema_view = get_swagger_view(title='api view')


admin.site.site_header = _(settings.ADMIN_SITE_HEADER)
admin.site.index_title = _(settings.ADMIN_SITE_HEADER)
admin.site.site_title = _(settings.ADMIN_SITE_HEADER)


def login_check(user):
    return user.is_anonymous()


def not_login_check(user):
    return not user.is_anonymous()


login_redirect = lazy(reverse, str)('doc')
not_login_redirect = lazy(reverse, str)('login')
login_view = auth_views.LoginView.as_view(template_name='accounts/login.html')
login_user_test_func = user_passes_test(login_check, login_redirect, redirect_field_name=None)
not_login_user_test_func = user_passes_test(not_login_check, not_login_redirect, redirect_field_name=None)

urlpatterns = [
    url(r'^$', not_login_user_test_func(login_view), name='root'),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webapp/', include('webapp.urls', namespace='pd')),
    url(r'^norns/', include('norns.urls', namespace='norns')),
    url(r'^accounts/', include('accounts.urls', namespace='account')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^login/$', login_user_test_func(login_view), name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^social/', include('social_django.urls', namespace='social')),
    url(r'^api/$', schema_view, name='doc')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
