from django.shortcuts import render
from .jsonresponse import JSONResponse
from patients_app.models.visits import Visit
from api.serializers.visit import VisitSerializer
from rest_framework import generics
from datetime import date

from patients_app.models.Patients import Patient

class VisitList(generics.ListAPIView):
    serializer_class = VisitSerializer

    def get_queryset(self):
        """
        This view should return a list of all the visits for
        the office.
        """
        queryset = Visit.objects.all()
        date_selected = self.request.query_params.get('date', None)
        office_pk = self.request.query_params.get('officepk', None)
        
        if date_selected is not None:
            date_list = date_selected.split('-')
            date_converted = date(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
            queryset = queryset.filter(date=date_converted)
        
        if office_pk is not None:
            patient_of_office = Patient.objects.filter(office = office_pk)
            visits_of_office = []
            for patient in patient_of_office:
                for soin in patient.treatments.all():
                    for visit in Visit.objects.filter(soin = soin):
                        if visit in queryset:
                            visits_of_office.append(visit)
            queryset = visits_of_office
        
        return queryset
        