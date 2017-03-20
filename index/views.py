from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

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
    #if request.user == 'AnonymousUser':
    #    return HttpResponseRedirect(reverse('login'))

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
    counter = get_object_or_404(Counter, user__username=user_name)
    try:
        print('POST: ' + request.POST['count'])
        counter.counter_for_day += int(request.POST['count'])
        counter.counter_for_all_time += int(request.POST['count'])
       # print(counter.counter_for_day)
        counter.save()
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('index:index'))

def sign_up(request):
    errors = []
    #form = RegisterForm()
    form = UserCreationForm()
    if request.POST:
        #form = RegisterForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.counter_set.create()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password2'])
            login(request, user)
            return HttpResponseRedirect(reverse('index:counter', args=[user.username]))
    return render(request, 'registration/sign_up.html', {'errors': errors, 'form': form})

def new_day():
    result = Counter.objects.all()
    for counter in result:
        #counter.counter_for_all_time += counter.counter_for_day
        counter.counter_for_day = 0
        counter.save()



