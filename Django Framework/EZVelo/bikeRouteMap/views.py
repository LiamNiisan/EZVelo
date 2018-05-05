from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def map(request):  
   #template = loader.get_template('map/index.html')
   #return render(request, "bikeRouteMap/template/map.html", {})
   #return HttpResponse("Hello, <b>world</b>. You're at the map index.")
   #return HttpResponse(template.render(request))
   #return render(request, 'map/index.html')
   return render(request, "map/index.html")
# Create your views here.
