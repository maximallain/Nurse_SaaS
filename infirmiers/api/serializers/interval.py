from rest_framework import serializers
from infirmiers_app.models.interval import Interval

class IntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interval
        fields = ('real_start_time', 'real_end_time')