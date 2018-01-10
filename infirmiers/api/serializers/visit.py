from rest_framework import serializers
from patients_app.models.visits import Visit

from .soins import SoinSerializer

class VisitSerializer(serializers.ModelSerializer):
    soin = serializers.SerializerMethodField()

    class Meta:
        model = Visit
        fields = ('date', 'completed', 'duration_visit', 'nurse', 'soin','pk')

    def get_soin(self, obj):
        serializer = SoinSerializer(obj.soin)
        return serializer.data