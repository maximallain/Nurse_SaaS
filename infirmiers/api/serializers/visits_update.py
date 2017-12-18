from rest_framework import serializers

class VisitPostSerializers(serializers.Serializer):
    visit_pk = serializers.IntegerField()
    nurse_pk = serializers.IntegerField()
    time = serializers.CharField()