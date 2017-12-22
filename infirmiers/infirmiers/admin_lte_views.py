from django.conf import settings
from django.http import HttpResponse


def bower_view(request, path):
    file_location = settings.BOWER_COMPONENTS + '/' + path
    file = open(file_location, 'r')
    doc = file.read()
    file.close()
    print(HttpResponse(doc))
    return HttpResponse(doc)

def dist_view(request,path):
    file_location = settings.DIST + '/' + path
    file = open(file_location, 'r')
    doc = file.read()
    file.close()
    return HttpResponse(doc)
