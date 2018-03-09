from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
# Create your views here.
def index(request):
    return render(request, "index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # if username == 'admin' and password == 'admin123':
        #     #return render(request, 'event_manager.html')
        #     response = HttpResponseRedirect('/event_manager/')
        #     #response.set_cookie('user', username, 3600)#设置cookies
        #     request.session['user'] = username #设置session
        #     return response
        # else:
        #     return render(request, "index.html", {'error': '用户名或密码错误'})
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manager/')
            return response
        else:
            return render(request, "index.html", {'error': '用户名或密码错误'})
@login_required()
def event_manager(request):
    #username = request.COOKIES.get('user') #获取cookies
    username = request.session.get('user') # 获取session
    event_list = Event.objects.all()
    return render(request, 'event_manager1.html', {'user': username,
                                                  'events': event_list})
@login_required()
def searchevent_manager(request):
    event_name = request.GET.get('event_name')
    if event_name is None:
        event_list = Event.objects.all()
    else:
        event_list = Event.objects.filter(name__contains=event_name)
    username = request.session.get('user')

    return render(request, 'event_manager1.html', {'events': event_list,
                                                  'user': username})
@login_required()
def guest_manager(request):
    guest_list = Guest.objects.all()
    #event_list = Event.objects.all()
    return render(request, 'guest_manager.html', {'guests': guest_list})
@login_required()
def searchguest_manager(request):
    guest_name = request.GET.get('guest_name')
    if guest_name is None:
        guest_list = Guest.objects.all()
    else:
        guest_list = Guest.objects.filter(realname__contains=guest_name)
    username = request.session.get('user')

    return render(request, 'guest_manager.html', {'guests': guest_list,
                                                   'user': username})