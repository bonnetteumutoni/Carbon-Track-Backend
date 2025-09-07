from django.db import models
from factory.models import Factory
from django.db.models import Sum
from decimal import Decimal

class EnergyEntry(models.Model):
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
