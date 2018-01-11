from django.shortcuts import render
from .jsonresponse import JSONResponse
from api.serializers.visits_update import VisitPostSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date, time

from patients_app.models.visits import Visit
from nurses_app.models.nurse import Nurse

class VisitsListPostAPIView(APIView):

    def post(self, request, format=None):
        serializer = VisitPostSerializers(data=request.data, many=True)
        if serializer.is_valid():
            for elt in serializer.data:
                visit_pk = elt['visit_pk']
                visit = Visit.objects.filter(pk = visit_pk)[0]

                nurse = Nurse.objects.filter(pk = elt['nurse_pk'])[0]
                visit.nurse = nurse

                start_time = elt['time'].split(':')
                start_time = time(hour=int(start_time[0]), minute=int(start_time[1]))
                visit.time = start_time
                
                visit.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)