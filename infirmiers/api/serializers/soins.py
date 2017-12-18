from rest_framework import serializers
from soins_app.models.soins import Soin
from .patients import PatientSerializer

class SoinSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    
    class Meta:
        model = Soin
        fields = ('patient',)

    
    def get_patient(self, obj):
        serializer = PatientSerializer(obj.patient)
        return serializer.data