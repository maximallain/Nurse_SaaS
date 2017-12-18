from rest_framework import serializers
from soins_app.models.soins import Soin
from soins_app.models.Patients import Patient
from .patients import PatientSerializer

class SoinSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    
    class Meta:
        model = Soin
        fields = ('patient',)

    
    def get_patient(self, obj):
        patient = Patient.objects.filter(treatments = obj)[0]
        serializer = PatientSerializer(patient)
        return serializer.data