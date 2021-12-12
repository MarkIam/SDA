import json
from django.http import JsonResponse
from django.shortcuts import render
from manifest.models import Skydiver, SkydiverRequest, PlaneLift, SkydiveDiscipline
from django.db.models import Q

def vue(request):
    return render(request, 'vue.html')
                
def manifest(request):
    skydivers_list = Skydiver.objects.all()
    return render(request, 'index.html',
                {
                  'skydivers_list': skydivers_list
                })

def skydiver_detail(request, id):
    skydiver = Skydiver.objects.get(pk = id)
    return render(request, 'detail.html',
                {
                  'skydiver': skydiver
                })

def unassigned_requests_list(request):
    discQueryset = SkydiveDiscipline.objects.all().order_by('id')
    
    disc_list =[]
    for disc in discQueryset:
        disc_list.append({
                    'id': disc.id,
                    'discipline_name': disc.short_name,
                    'requests': [] })
    
    current_discipline_id = -1
    current_discipline = {}
    request_pool =[]

    reqQueryset = SkydiverRequest.objects.filter(status='CR').order_by('discipline')
    for req in reqQueryset:
        if not (req.planelift_set.exists()):
            if req.discipline.id != current_discipline_id:
                if current_discipline_id != -1:
                    current_discipline['requests'] = request_pool

                for index, item in enumerate(disc_list):
                    if item['id'] == req.discipline.id:
                        break
                else:
                    index = -1
                current_discipline = disc_list[index]
                current_discipline_id = req.discipline.id
                request_pool =[]

            request_pool.append({
                'id': req.id,
                'skydiver_name': req.skydiver.last_name + ' ' + req.skydiver.first_name,
                'discipline_id': req.discipline.id,
                'discipline_name': req.discipline.name,
                'height': req.height,
                'creationStamp': req.creationStamp.strftime("%d.%m.%Y, %H:%M")
            })
    
    current_discipline['requests'] = request_pool

    return JsonResponse(disc_list, safe=False)

def lifts_list(request):
    pDay = request.GET.get('pDay', '')
    queryset = PlaneLift.objects.filter(day = pDay).filter(~Q(status='CMP') & ~Q(status='CNC')).order_by('ord_number')
    ret = []
    for lift in queryset:
        reqs = []
        for req in lift.request.all():
            reqs.append({
                'id': req.id,
                'skydiver_name': req.skydiver.last_name + ' ' + req.skydiver.first_name,
                'discipline_id': req.discipline.id,
                'discipline_name': req.discipline.name,
                'height': req.height,
                'creationStamp': req.creationStamp.strftime("%d.%m.%Y, %H:%M")
            })
        ret.append({
            'id':lift.id,
            'ord_number':lift.ord_number,
            'plane_reg_number':lift.plane.reg_number,
            'lift_date':lift.day,
            'requests': reqs,
            'visible': True if len(ret) == 0 else False
        })
    return JsonResponse(ret,safe=False)

def bind_request_to_lift(request):
    data =(json.loads(request.body))
    request_id = data['request_id']
    lift_id = data['lift_id']
    is_bind = data['is_bind']

    lift = PlaneLift.objects.get(pk=lift_id)
    request = SkydiverRequest.objects.get(pk=request_id)
    try:
        if (is_bind):
            lift.request.add(request)
        else:
            lift.request.remove(request)
        lift.save()
    except Exception:
        return JsonResponse({'status':'not OK'})
    
    return JsonResponse({'status':'OK'})