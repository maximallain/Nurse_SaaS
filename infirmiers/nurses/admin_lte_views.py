from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse
from django.http import JsonResponse

def static(request, path):
    file_location = settings.STATIC_URL + '/' + path
    file = open(file_location, 'r')
    doc = file.read()
    file.close()
    return JsonResponse(doc)

def dist_view(request,path):
    file_location = settings.DIST + '/' + path
    file = open(file_location, 'r')
    doc = file.read()
    file.close()
    return HttpResponse(doc, content_type='text/javascript')
