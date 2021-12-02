from django.http import JsonResponse
from django.shortcuts import render
from manifest.models import Skydiver, SkydiverRequest, PlaneLift
from django.db.models import Q

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
    queryset = SkydiverRequest.objects.filter(status='CR').order_by('discipline')
    ret =[]
    for req in queryset:
        ret.append({
            'id':req.id,
            'skydiver_name':req.skydiver.last_name,
            'discipline_name':req.discipline.name,
            'discipline_short_name':req.discipline.short_name
        })
    return JsonResponse(ret,safe=False)

def lifts_list(request):
    queryset = PlaneLift.objects.filter(~Q(status='CMP') & ~Q(status='CNC')).order_by('ord_number')
    ret =[]
    for lift in queryset:
        ret.append({
            'id':lift.id,
            'ord_number':lift.ord_number,
            'plane_reg_number':lift.plane.reg_number,
            'lift_date':lift.day
        })
    return JsonResponse(ret,safe=False)