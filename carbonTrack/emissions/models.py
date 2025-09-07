from django.db import models
from django.db.models import Sum
from factory.models import Factory


class Emissions(models.Model):
    emissions_id = models.AutoField(primary_key=True)
    device_id = models.CharField(max_length=255)
    emission_rate = models.DecimalField(max_digits=15, decimal_places=15)
    updated_at = models.DateTimeField(auto_now=True)

    factory = models.ForeignKey(
        Factory,
        on_delete=models.CASCADE,
        related_name='emissions',
        null=True, 
        blank=True
    )

    @staticmethod
    def assign_factory_based_on_device(device_id):
        if device_id.startswith('ESP32-') and all(c == '0' for c in device_id[4:]):
            return Factory.objects.get(factory_id=67)
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.factory_id:
            assigned_factory = self.assign_factory_based_on_device(self.device_id)
            if assigned_factory:
                self.factory = assigned_factory
        super().save(*args, **kwargs)

    @staticmethod
    def get_emission_sum_by_factory_and_date(factory_id, date):
        emissions = Emissions.objects.filter(
            factory_id=factory_id,
            updated_at__date=date
        ).aggregate(total_emission=Sum('emission_rate'))
        return emissions['total_emission'] or 0

    def __str__(self):
        return f"{self.device_id} - {self.emission_rate}"
