from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
def index(request):
    return render(request, "index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
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
            #设置session过期时间
            #request.session.set_expiry(20)
            response = HttpResponseRedirect('/event_manager/')
            return response
        else:
            return render(request, "index.html", {'error': '用户名或密码错误'})
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')
@login_required()
def event_manager(request):
    #username = request.COOKIES.get('user') #获取cookies
    username = request.session.get('user') # 获取session
    event_list = Event.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(event_list, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'event_manager1.html', {'user': username,
                                                  'events': contacts})
@login_required()
def searchevent_manager(request):
    event_name = request.GET.get('event_name')
    if event_name is None:
        event_list = Event.objects.all()
    else:
        event_list = Event.objects.filter(name__contains=event_name)
    username = request.session.get('user')
    paginator = Paginator(event_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'event_manager1.html', {'events': contacts,
                                                  'user': username})
@login_required()
def guest_manager(request):
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    #event_list = Event.objects.all()
    return render(request, 'guest_manager.html', {'guests': contacts})
@login_required()
def searchguest_manager(request):
    guest_name = request.GET.get('guest_name')
    #guest_list = Guest.objects.get(realname=guest_name)
    #guest_list = get_object_or_404(Guest, realname=guest_name)
    if guest_name is None:
        guest_list = Guest.objects.all()

    else:
        guest_list = Guest.objects.filter(realname__contains=guest_name)
    username = request.session.get('user')
    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manager.html', {'guests': contacts,
                                                   'user': username})
@login_required()
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', {'event': event})

@login_required()
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone')
    # print("手机号为：" + phone)
    # print(type(phone))
    # if phone is '':
    #     return render(request, 'sign_index.html', {'hint': '请输入手机号.'})
    if event.status is False:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event is end.'})
    result = Guest.objects.get(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has sign in."})
    else:
        #Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        a = Guest.objects.get(phone=phone, event_id=event_id)
        a.sign = '1'
        a.save()
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'guest': result})
@login_required()
def add_guest(request):
    event_list = Event.objects.all()
    return render(request, 'register.html', {'events': event_list})

@login_required()
def add_guest_submit(request):
    realname = request.POST.get('realname')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    event_name = request.POST.get('event_name')
    print("==============" + event_name)
    event_id = Event.objects.get(name=event_name).id
    Guest.objects.create(realname=realname, phone=phone, email=email, event_id=event_id, sign=False)
    return HttpResponseRedirect('/guest_manage/')

@login_required()
def delete_guest(request, guest_id):
    Guest.objects.get(id=guest_id).delete()
    return HttpResponseRedirect("/guest_manage")

@login_required()
def event_guest(request, event_id):
    guest_list = Guest.objects.filter(event_id=event_id)
    return render(request, "guest_manager.html", {'guests': guest_list})


def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password_conf = request.POST.get('password_conf', '')
        email = request.POST.get('email', '')
        registerForm = Regi









