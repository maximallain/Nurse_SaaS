from rest_framework import serializers
from soins_app.models.visits import Visit

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ('date', 'completed', 'duration_visit', 'nurse')