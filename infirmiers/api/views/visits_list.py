from django.shortcuts import render
from .jsonresponse import JSONResponse
from soins_app.models.visits import Visit
from api.serializers.visit import VisitSerializer
from rest_framework import generics
from datetime import date

class VisitList(generics.ListAPIView):
    serializer_class = VisitSerializer

    def get_queryset(self):
        """
        This view should return a list of all the visits for
        the office.
        """
        queryset = Visit.objects.all()
        try:
            date_selected = self.kwargs['date']
            date_list = date_selected.split('-')
            date_converted = date(year=int(date_list[0]), month=int(date_list[1]), day=int(date_list[2]))
            queryset = queryset.filter(date=date_converted)
            return queryset
        except KeyError:
            return queryset
        