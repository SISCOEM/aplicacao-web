from rest_framework import serializers
from .models import Load, Equipment_load
from police.serializers import PoliceSerializer
from equipment.serializers import EquipmentSerializer, BulletSerializer, ArmamentModelSerializer
from django.utils import timezone        
class LoadSerializer(serializers.ModelSerializer):
    police_adjunct = PoliceSerializer(source='adjunct', read_only=True)
    formatted_load_date = serializers.SerializerMethodField()
    formatted_expected_discharge_date = serializers.SerializerMethodField()
    itemsQuantity = serializers.SerializerMethodField()
    class Meta:
        model = Load
        fields = '__all__'
    

    def get_formatted_load_date(self, obj):
        date = obj.date_load
        if date is not None:
            date = date.astimezone(timezone.get_current_timezone())
            return date.strftime("%d-%m-%Y %H:%M")
        
    def get_formatted_expected_discharge_date(self, obj):
        date = obj.expected_load_return_date
        if date is not None:            
            date = date.astimezone(timezone.get_current_timezone())         
            return date.strftime("%d-%m-%Y %H:%M")

    def get_itemsQuantity(self, obj):
        load_id = obj.id
        if load_id is not None:
            items_load = Equipment_load.objects.filter(load_id=load_id)
            return len(items_load)
        
        
class Equipment_loadSerializer(serializers.ModelSerializer):
    bullet = BulletSerializer(read_only=True)
    equipment = EquipmentSerializer(read_only=True)
    armament_model = ArmamentModelSerializer( read_only=True)

    class Meta:
        model = Equipment_load
        fields = ['amount','observation', 'status', 'bullet', 'equipment', 'armament_model'] # Selecionar os campos
        
    
        
    