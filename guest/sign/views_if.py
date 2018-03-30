from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import  IntegrityError
from datetime import datetime
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
        return JsonResponse({'status': 10022, 'm    essage': 'event id already exists'})
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

#发布会查询接口
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

#添加嘉宾
def add_guest(request):
    eid = request.POST.get('eid', '')
    realname = request.POST.get('realname', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    if eid == '' or realname == '' or phone == '':
        print(eid)
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})
    event_limit = Event.objects.get(id=eid).limit
    guest_num = Guest.objects.filter(event_id=eid)

    if event_limit < len(guest_num):
        return JsonResponse({'status': 10024, 'message': 'event limit is full'})

    event_time = Event.objects.get(id=eid).start_time
    e_time = event_time.timestamp() #发布会时间
    n_time = datetime.now().timestamp() #当前时间
    print(e_time)
    print(n_time)
    if e_time > n_time:
        return JsonResponse({'status': 10025, 'message': 'event has started'})

    try:
        Guest.objects.create(realname=realname, event_id=eid, phone=phone, email=email, sign=1)

    except IntegrityError:
        return JsonResponse({'status': 10026, 'message': 'the event guest phone number repeat'})

    else:
        return JsonResponse({'status': 200, 'message': 'add guest success'})

