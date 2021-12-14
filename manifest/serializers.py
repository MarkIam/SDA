from rest_framework import serializers
from manifest.models import SkydiveDiscipline, SkydiverRequest, PlaneLift

class SkydiverRequestSerializer(serializers.ModelSerializer):
    skydiver_last_name = serializers.CharField(source='skydiver.last_name', max_length=64)
    skydiver_first_name = serializers.CharField(source='skydiver.first_name', max_length=64)
    discipline_name = serializers.CharField(source='discipline.name', max_length=64)
    creationStamp = serializers.DateTimeField(format="%d.%m.%Y, %H:%M")

    class Meta:
        model = SkydiverRequest
        fields = ['id', 'skydiver_last_name', 'skydiver_first_name', 'discipline_id', 'discipline_name', 'height', 'creationStamp']

class SkydiveDisciplineSerializer(serializers.ModelSerializer):
    skydiverrequest_set = SkydiverRequestSerializer(many=True)
    class Meta:
        model = SkydiveDiscipline
        fields = ['id', 'name', 'short_name', 'skydiverrequest_set']

class PlaneLiftSerializer(serializers.ModelSerializer):
    plane_reg_number = serializers.CharField(source='plane.reg_number', max_length=64)
    lift_date = serializers.DateField(source='day')
    request = SkydiverRequestSerializer(many=True)
    
    class Meta:
        model = PlaneLift
        fields = ['id', 'ord_number', 'plane_reg_number', 'lift_date', 'request']