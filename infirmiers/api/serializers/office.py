from rest_framework import serializers
from signUp.models.office import Office

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('adress', 'user')