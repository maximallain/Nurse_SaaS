from django.shortcuts import render
from .jsonresponse import JSONResponse
from infirmiers_app.models.nurse import Nurse
from api.serializers.nurse import NurseSerializers
from signUp.models.office import Office
from rest_framework import generics

class NursesList(generics.ListAPIView):
    serializer_class = NurseSerializers

    def get_queryset(self):
        """
        This view should return a list of all the nurses for
        the office.
        """
        queryset = Nurse.objects.all()
        try:
            office_pk = self.kwargs['officepk']
            office = Office.objects.filter(pk = office_pk)
            queryset = queryset.filter(office=office)
            return queryset
        except KeyError:
            return queryset



