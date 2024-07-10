from rest_framework import serializers
from .models import Police

class PoliceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Police
        fields = ['id', 'name', 'posto']
    
    