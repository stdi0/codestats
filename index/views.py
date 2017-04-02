from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.db import IntegrityError

from datetime import datetime
import urllib.request
import urllib.parse
import json

from .models import Counter

def index(request):
    if request.user.is_authenticated():

        #Figure out position in rating
        result = Counter.objects.all().order_by('-counter_for_day')
        for n, count in enumerate(result):
            if count.user.username == request.user.username:
                rating_day = n + 1
                break;
        result = Counter.objects.all().order_by('-counter_for_all_time')
        for n, count in enumerate(result):
            if count.user.username == request.user.username:
                rating_alltime = n + 1
                break;

        counter = get_object_or_404(Counter, user__username=request.user.username)
        context = {'counter': counter, 'rating_day': rating_day, 'rating_alltime': rating_alltime}
        return render(request, 'index/mycounter.html', context)
    return HttpResponseRedirect(reverse('login'))

def counter(request, user_name):

    #Figure out position in rating
    result = Counter.objects.all().order_by('-counter_for_day')

    for n, count in enumerate(result):
        if count.user.username == user_name:
            rating_day = n + 1
            break;
    result = Counter.objects.all().order_by('-counter_for_all_time')
    for n, count in enumerate(result):
        if count.user.username == user_name:
            rating_alltime = n + 1
            break;

    counter = get_object_or_404(Counter, user__username=user_name)
    context = {'counter': counter, 'rating_day': rating_day, 'rating_alltime': rating_alltime}
    return render(request, 'index/counter.html', context)

def topday(request):
    try:
        result = Counter.objects.all().order_by('-counter_for_day')

        #Update rating
        for pos, count in enumerate(result):
            count.pos = pos + 1

        paginator = Paginator(result, 10)
        page = request.GET.get('page')
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
    except:
        pass
    context = {'result': result}
    return render(request, 'index/topday.html', context)


def topall(request):
    try:
        result = Counter.objects.all().order_by('-counter_for_all_time')

        #Update rating
        for pos, count in enumerate(result):
            count.pos = pos + 1

        paginator = Paginator(result, 10)
        page = request.GET.get('page')
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
    except:
        pass
    context = {'result': result}
    return render(request, 'index/topall.html', context)

@csrf_exempt
def api_call(request, user_name):
    user = authenticate(username=user_name, password=request.POST['password'])
    if user is not None:
        counter = get_object_or_404(Counter, user__username=user_name)
        try:
            counter.counter_for_day += int(request.POST['count'])
            counter.counter_for_all_time += int(request.POST['count'])
            counter.save()
        except:
            pass
    return HttpResponseRedirect(reverse('index'))

def sign_up(request):
    errors = []
    form = UserCreationForm()
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.counter_set.create()
            #user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
            user = authenticate(username=form.cleaned_data['username'])
            login(request, user)
            return HttpResponseRedirect(reverse('counter', args=[user.username]))
    return render(request, 'registration/sign_up.html', {'errors': errors, 'form': form})

def new_day():
    result = Counter.objects.all()
    for counter in result:
        counter.counter_for_day = 0
        counter.save()

client_id = 'c23c344c20e7ca5f6b61'
client_secret = '773f43356a7f3368a008a8aa91e65b12f55a682d'
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

def login_with_github(request):
    authorization_url = authorization_base_url + '/?client_id=' + client_id
    return HttpResponseRedirect(authorization_url)

def link_github(request):
    authorization_url = authorization_base_url + '/?client_id=' + client_id
    return HttpResponseRedirect(authorization_url)

def callback(request):
    #try:
    data = urllib.parse.urlencode({'client_id': client_id, 'client_secret': client_secret, 'code': request.GET['code']}).encode()
    assembled_request = urllib.request.Request(token_url, data=data, headers={
        'Accept': 'application/json'
    })
    resp = urllib.request.urlopen(assembled_request)
    string = resp.read().decode('utf-8')
    json_obj = json.loads(string)

    resp = urllib.request.urlopen('https://api.github.com/user?access_token=' + json_obj['access_token'])
    string = resp.read().decode('utf-8')
    json_obj = json.loads(string)

    #data = urllib.parse.urlencode({'username': 'test12345', 'password1': 'joo0shaij', 'password2': 'joo0shaij'}).encode()
    #request = urllib.request.Request('http://codestats.pythonanywhere.com/sign_up', data=data)
    #counter = Counter.objects.filter(github_login=json_obj['login'])
    
    if request.user.is_authenticated():
        user = request.user
        old_links = User.objects.filter(counter__github_login=json_obj['login'])
        old_links.delete()
        user.counter__github_login = json_obj['login']
        user.save()
        return HttpResponseRedirect(reverse('index'))

    user = User.objects.filter(counter__github_login=json_obj['login'])
    #user = ''
    #try:
    #    user = counter.user
    #    return HttpResponse()
    #except:
    #    pass
    if not user:
        try:
            username = json_obj['login']
            u = User(username=username)
            u.set_password('password')
            u.save()
        except:
            i = 2
            while True:
                try:
                    username = json_obj['login'] + str(i)
                    u = User(username=username)
                    u.set_password('password')
                    u.save()
                    break
                except:
                    i += 1
        u.counter_set.create(github_login=json_obj['login'])
        #user = authenticate(username=json_obj['login'], password='password')
        user = authenticate(username=json_obj['login'])
        login(request, user)
        return HttpResponseRedirect(reverse('change_password'))
    else:
        #user.backend = 'django.contrib.auth.backends.ModelBackend'
        user = authenticate(username=user[0].username)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    #except:
    #    pass
    

def change_password(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('index')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'registration/change_password.html', {
            'form': form
        })
    return HttpResponseRedirect(reverse('login'))

def settings(request):
    if request.user.is_authenticated():
        context = {}
        return render(request, 'index/settings.html', context)
    return HttpResponseRedirect(reverse('login'))









