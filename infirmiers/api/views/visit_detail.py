from django.shortcuts import render
from .jsonresponse import JSONResponse
from patients_app.models.visits import Visit
from api.serializers.visit import VisitSerializer

def visit_detail(request, pk):
    try:
        visit = Visit.objects.get(pk=pk)
    except Visit.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = VisitSerializer(visit)
        return JSONResponse(serializer.data)