from django.shortcuts import render
from .jsonresponse import JSONResponse
from infirmiers_app.models.nurse import Nurse
from api.serializers.nurse import NurseSerializers

def nurse_detail(request, pk):
    try:
        nurse = Nurse.objects.get(pk=pk)
    except Nurse.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NurseSerializers(nurse)
        return JSONResponse(serializer.data)