import json
from django.http import JsonResponse
from django.shortcuts import render
from manifest.models import Skydiver, SkydiverRequest, PlaneLift, SkydiveDiscipline
from django.db.models import Q
from manifest.serializers import SkydiverRequestSerializer, SkydiveDisciplineSerializer, PlaneLiftSerializer


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

from rest_framework import viewsets

class SkydiverRequestViewSet(viewsets.ModelViewSet):
    queryset = SkydiverRequest.objects.all()
    serializer_class = SkydiverRequestSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status='CR').filter(planelift__isnull=True)
        return queryset

class SkydiveDisciplineViewSet(viewsets.ModelViewSet):
    queryset = SkydiveDiscipline.objects.all()
    serializer_class = SkydiveDisciplineSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('id')
        return queryset

class PlaneLiftViewSet(viewsets.ModelViewSet):
    queryset = PlaneLift.objects.all()
    serializer_class = PlaneLiftSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        pDay = self.request.GET.get('pDay','')
        if pDay:
            queryset = queryset.filter(day = pDay).filter(~Q(status='CMP') & ~Q(status='CNC')).order_by('ord_number')
        return queryset