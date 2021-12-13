from rest_framework import serializers
from manifest.models import SkydiveDiscipline, SkydiverRequest
#, PlaneLift

class SkydiverRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkydiverRequest
        fields ="__all__"

class SkydiveDisciplineSerializer(serializers.ModelSerializer):
    #request_set = SkydiverRequestSerializer(many=True)
    class Meta:
        model = SkydiveDiscipline
        fields ="__all__"