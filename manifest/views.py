from django.http import JsonResponse
from django.shortcuts import render
from manifest.models import Skydiver, SkydiverRequest

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
            'discipline_name':req.discipline.name
        })
    return JsonResponse(ret,safe=False)