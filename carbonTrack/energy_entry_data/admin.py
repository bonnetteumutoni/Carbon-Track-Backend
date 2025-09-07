from django.contrib import admin
from energy_entry_data.models import EnergyEntry

admin.site.register(EnergyEntry)

def get_readonly_fields(self, request, obj=None):
        
        readonly = list(super().get_readonly_fields(request, obj))
        if 'co2_equivalent' not in readonly:
            readonly.append('co2_equivalent')
        return readonly