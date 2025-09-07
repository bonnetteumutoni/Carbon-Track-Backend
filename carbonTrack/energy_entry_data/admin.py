from django.contrib import admin
<<<<<<< HEAD
from energy_entry_data.models import EnergyEntry

admin.site.register(EnergyEntry)

def get_readonly_fields(self, request, obj=None):
        
        readonly = list(super().get_readonly_fields(request, obj))
        if 'co2_equivalent' not in readonly:
            readonly.append('co2_equivalent')
        return readonly
=======
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
>>>>>>> d7822e02be4605c4f0093b89a0afe86acc294ca4
