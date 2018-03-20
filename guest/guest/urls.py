"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from sign import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
    url(r'^$', views.index),
    url(r'^login_action/$', views.login_action),
    url(r'^event_manager/$', views.event_manager),
    url(r'^accounts/login/$', views.index),
    url(r'^event_manager/event_name/', views.searchevent_manager),
    url(r'^guest_manage/$', views.guest_manager),
    url(r'^guest_manage/guest_name', views.searchguest_manager),
    url(r'^logout/', views.logout),
    url(r'^sign_index/(?P<event_id>[0-9]+)/$', views.sign_index),
    url(r'^sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action),
    url(r'^add_guest/$', views.add_guest),
    url(r'^add_guest_submit/$', views.add_guest_submit),
    url(r'^delete_guest/(?P<guest_id>[0-9]+)$', views.delete_guest),
    url(r'^event_guest/(?P<event_id>[0-9]+)$', views.event_guest),
    url(r'^register/$', views.register_user),

    #不通过view视图直接跳转html
    url(r'^register_go/$', TemplateView.as_view(template_name='register.html')),

]
