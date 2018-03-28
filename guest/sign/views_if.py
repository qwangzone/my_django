from django.http import JsonResponse
from sign.models import Event
from django.core.exceptions import ValidationError

#添加发布会接口
def add_event(request):
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')
    Event.objects.create(id=eid, name=name, status=status, address=address)
