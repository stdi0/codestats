"""codestats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from index import views
from django.views.static import serve

urlpatterns = [
    #url(r'^', include('index.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    #url(r'^login/$', auth_views.login, name='login'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^login_with_github/$', views.login_with_github, name='login_with_github'),
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^top/day$', views.topday, name='topday'),
    url(r'^top/all$', views.topall, name='topall'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_name>\d*[a-zA-Z]+\d*)/api_call/$', views.api_call, name='api_call'),
    url(r'^(?P<user_name>\d*[a-zA-Z]+\d*)/$', views.counter, name='counter'),
    url(r'image/(?P<path>.*)$', serve, {'document_root': settings.STATIC_DOC_ROOT }),
]
