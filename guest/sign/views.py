from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request, "index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == 'admin' and password == 'admin123':
            #return render(request, 'event_manager.html')
            response = HttpResponseRedirect('/event_manager/')
            #response.set_cookie('user', username, 3600)#设置cookies
            request.session['user'] = username #设置session
            return response
        else:
            return render(request, "index.html", {'error': '用户名或密码错误'})

def event_manager(request):
    #username = request.COOKIES.get('user') #获取cookies
    username = request.session.get('user') # 获取session
    return render(request, 'event_manager.html', {'user': username})
