from django.contrib import admin
from .models import EnergyEntryData

admin.site.register(EnergyEntryData)
class EnergyEntryDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'factory_name', 'energy_type', 'energy_amount_with_unit', 'tea_processed_kg', 'co2_equivalent', 'created_at')
    list_filter = ('energy_type', 'created_at')
    search_fields = ('factory__factory_name', 'energy_type')
    ordering = ('-created_at',)

    def energy_amount_with_unit(self, obj):
        unit = obj.get_energy_unit()
        return f"{obj.energy_amount} {unit}"
    energy_amount_with_unit.short_description = 'Energy Amount'

    def factory_name(self, obj):
        return obj.factory.factory_name if obj.factory else "No Factory"
    factory_name.admin_order_field = 'factory__factory_name'
    factory_name.short_description = 'Factory'
