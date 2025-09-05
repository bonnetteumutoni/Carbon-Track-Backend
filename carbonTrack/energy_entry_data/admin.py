# admin.py

from django.contrib import admin
from .models import EnergyEntryData

@admin.register(EnergyEntryData)
class EnergyEntryDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_factory_name', 'energy_type', 'energy_amount_with_unit', 'tea_processed_kg', 'co2_equivalent', 'created_at')
    list_filter = ('energy_type', 'created_at')
    search_fields = ('user__factory__factory_name', 'energy_type')
    ordering = ('-created_at',)

    def energy_amount_with_unit(self, obj):
        unit = obj.get_energy_unit()
        return f"{obj.energy_amount} {unit}"
    energy_amount_with_unit.short_description = 'Energy Amount'

    def user_factory_name(self, obj):
        factory = getattr(obj.user, 'factory', None)
        return factory.factory_name if factory else "No Factory"
    user_factory_name.short_description = 'Factory'
