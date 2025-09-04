from rest_framework import serializers
from .models import EnergyEntryData

class EnergyEntryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyEntryData
        fields = '__all__'  
        read_only_fields = ['co2_equivalent', 'created_at', 'updated_at']
