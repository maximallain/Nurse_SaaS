from rest_framework import serializers
from infirmiers_app.models.nurse import Nurse
from .interval import IntervalSerializer
from .office import OfficeSerializer

class NurseSerializers(serializers.ModelSerializer):
    intervals = serializers.SerializerMethodField()
    office = serializers.SerializerMethodField()
    
    class Meta:
        model = Nurse
        fields = ('pk', 'FirstName', 'LastName', 'Gender', 'office', 'intervals')

    def get_intervals(self, obj):
        result = {}
        for interval in obj.intervals.all():
            serializer = IntervalSerializer(interval)
            if interval.weekday not in result:
                result[interval.weekday] = []
            result[interval.weekday].append(serializer.data)  
        return result

    def get_office(self, obj):
        serializer = OfficeSerializer(obj.office)
        return serializer.data