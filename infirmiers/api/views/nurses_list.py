from django.shortcuts import render
from .jsonresponse import JSONResponse
from infirmiers_app.models.nurse import Nurse
from api.serializers.nurse import NurseSerializers

def nurses_list(request):
    if request.method == 'GET':
        nurses = Nurse.objects.all()
        serializer = NurseSerializers(nurses, many=True)
        return JSONResponse(serializer.data)