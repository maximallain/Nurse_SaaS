from django.shortcuts import render
from .jsonresponse import JSONResponse
from soins_app.models.visits import Visit
from api.serializers.visit import VisitSerializer

def visits_list(request):
    if request.method == 'GET':
        visits = Visit.objects.all()
        serializer = VisitSerializer(visits, many=True)
        return JSONResponse(serializer.data)