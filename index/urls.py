from django.conf.urls import url

from . import views

app_name = 'index'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user_name>[a-zA-Z]+)/$', views.counter, name='counter'),
    url(r'^(?P<user_name>[a-zA-Z]+)/api_call/$', views.api_call, name='api_call'),
    #url(r'sign_up/$', views.sign_up, name='sign_up'),
]
