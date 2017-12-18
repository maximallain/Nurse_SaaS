from rest_framework import serializers
from soins_app.models.Patients import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('adresse',)