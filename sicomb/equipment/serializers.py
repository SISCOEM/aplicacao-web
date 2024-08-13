from .models import Equipment, Bullet, Model_armament
from rest_framework import serializers

class BulletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bullet
        fields = ['image_path', 'description']
        
class EquipmentSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipment
        fields = ['image_path', 'description'] # Selecionar os campos

    def get_image_path(self, obj):
        model_id = obj.model_id
        if model_id is not None:
            model_armament = Model_armament.objects.filter(id=model_id).first()
            if model_armament is not None:
                return str(model_armament.image_path)
        return None
    def get_description(self, obj):
        model_id = obj.model_id
        if model_id is not None:
            model_armament = Model_armament.objects.filter(id=model_id).first()
            if model_armament is not None:
                return model_armament.description
        return None
    
class ArmamentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_armament
        fields = ['image_path', 'description']
        