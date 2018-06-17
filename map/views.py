from django.shortcuts import render
from django.conf import settings

# Create your views here.

def index(request):
    args = {'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN}
    return render(request, 'map/index.html', args)