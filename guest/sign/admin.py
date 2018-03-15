from django.contrib import admin
from sign.models import Event, Guest, User
# Register your models here.


class EventAdmin(admin.ModelAdmin):

    list_display = ['name', 'status', 'start_time', 'id']
    search_fields = ['name']
    list_filter = ['status']


class GuestAdmin(admin.ModelAdmin):

    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['realname', 'phone']
    list_filter = ['sign']


class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'phone']

admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(User, UserAdmin)