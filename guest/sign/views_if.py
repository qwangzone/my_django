from django.http import JsonResponse
from sign.models import Event
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import json
#添加发布会接口
def add_event(request):
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')
    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    result = Event.objects.filter(eid=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})
    if status == '':
        status = 1
    try:
        Event.objects.create(id=eid, name=name, status=int(status), address=address, start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error. it must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': error})

#添加发布会查询接口
def get_event_list(request):
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')
    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['id'] = result.id
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})
    if name != '':
        data = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for eve in results:
                event = {}
                event['id'] = eve.id
                event['name'] = eve.name
                event['limit'] = eve.limit
                event['status'] = eve.status
                event['address'] = eve.address
                event['start_time'] = eve.start_time
                data.append(event)

            return JsonResponse({'status': 200, 'message': 'success', 'data': data})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})