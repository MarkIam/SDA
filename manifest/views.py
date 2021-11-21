from django.shortcuts import render
from manifest.models import Skydiver

def manifest(request):
    skydivers_list = Skydiver.objects.all()
    return render(request, 'index.html',
                {
                  'skydivers_list': skydivers_list
                })