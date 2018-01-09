from rest_framework import serializers
from soins_app.models.Patients import Patient
from .office import OfficeSerializer

class PatientSerializer(serializers.ModelSerializer):
    office = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = ('Adress','office')
    
    def get_office(self, obj):
        serializer = OfficeSerializer(obj.office)
        return serializer.data
