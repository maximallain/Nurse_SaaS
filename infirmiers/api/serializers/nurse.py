from rest_framework import serializers
from infirmiers_app.models.nurse import Nurse
from .interval import IntervalSerializer

class NurseSerializers(serializers.ModelSerializer):
    #intervals = IntervalSerializer(many=True, read_only=True)
    intervals = serializers.SerializerMethodField()
    
    class Meta:
        model = Nurse
        fields = ('FirstName', 'LastName', 'Gender', 'Office', 'intervals')

    def get_intervals(self, obj):
        result = {}
        for interval in obj.intervals.all():
            serializer = IntervalSerializer(interval)
            if interval.weekday not in result:
                result[interval.weekday] = []
            result[interval.weekday].append(serializer.data)  
        return result