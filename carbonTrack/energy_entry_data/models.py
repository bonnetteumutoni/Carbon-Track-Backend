from django.db import models
from factory.models import Factory


class EnergyEntryData(models.Model):
    ENERGY_TYPE_CHOICES = [
        ('electricity', 'Electricity'),
        ('diesel', 'Diesel'),
        ('firewood', 'Firewood'),
    ]

    UNITS = {
        'electricity': 'kWh',
        'diesel': 'liters',
        'firewood': 'kg',
    }

    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='energy_entries')
    energy_type = models.CharField(max_length=100, choices=ENERGY_TYPE_CHOICES)
    energy_amount = models.DecimalField(max_digits=15, decimal_places=4)
    tea_processed_kg = models.DecimalField(max_digits=15, decimal_places=4)
    co2_equivalent = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_energy_unit(self):
        return self.UNITS.get(self.energy_type, '')

    EMISSION_FACTORS = {
        'electricity': 0.233,  
        'diesel': 2.68,        
        'firewood': 0.41,      
    }

    def calculate_co2_equivalent(self):
        factor = self.EMISSION_FACTORS.get(self.energy_type.lower())
        if factor is None:
            raise ValueError(f"No emission factor defined for energy type '{self.energy_type}'")
        return float(self.energy_amount) * factor

    def save(self, *args, **kwargs):
        self.co2_equivalent = self.calculate_co2_equivalent()
        super().save(*args, **kwargs)

    def __str__(self):
        unit = self.get_energy_unit()
        return f"{self.energy_type.title()} - {self.energy_amount} {unit} for Factory: {self.factory.factory_name}"
