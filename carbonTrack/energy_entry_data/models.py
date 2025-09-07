from django.db import models
from factory.models import Factory
<<<<<<< HEAD
from django.db.models import Sum
from decimal import Decimal

class EnergyEntry(models.Model):
=======


class EnergyEntryData(models.Model):
>>>>>>> d7822e02be4605c4f0093b89a0afe86acc294ca4
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

<<<<<<< HEAD
    data_id = models.AutoField(primary_key=True)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    energy_type = models.CharField(max_length=100, choices=ENERGY_TYPE_CHOICES)
    energy_amount = models.DecimalField(max_digits=10, decimal_places=4)
    co2_equivalent = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True, editable=False)
    tea_processed_amount = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CO2_FACTORS = {
        'diesel': Decimal('2.7'),
        'fuel': Decimal('2.3'),
        'firewood': Decimal('1.8'),
        'electricity': Decimal('0.019'),
    }

    def save(self, *args, **kwargs):
        factor = self.CO2_FACTORS.get(self.energy_type.lower(), Decimal('0'))
        self.co2_equivalent = self.energy_amount * factor
        super().save(*args, **kwargs)

    @staticmethod
    def get_co2_sum_by_factory_and_date(factory_id, date):
        result = EnergyEntry.objects.filter(factory_id=factory_id, updated_at__date=date).aggregate(total_co2=Sum('co2_equivalent'))
        return result['total_co2'] or 0

    @staticmethod
    def get_tea_processed_sum_by_factory_and_date(factory_id, date):
        result = EnergyEntry.objects.filter(factory_id=factory_id, updated_at__date=date).aggregate(total_tea=Sum('tea_processed_amount'))
        return result['total_tea'] or 0
=======
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

    @classmethod
    def total_co2_emissions(cls):
        from django.db.models import Sum
        result = cls.objects.aggregate(total_emission=Sum('co2_equivalent'))
        return result['total_emission'] or 0

    def __str__(self):
        unit = self.get_energy_unit()
        factory_name = self.factory.factory_name if self.factory else "No Factory"
        return f"{self.energy_type.title()} - {self.energy_amount} {unit} for Factory: {factory_name}"
>>>>>>> d7822e02be4605c4f0093b89a0afe86acc294ca4
