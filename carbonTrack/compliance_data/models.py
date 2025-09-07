from django.db import models
from factory.models import Factory
from emissions.models import Emissions
from energy_entry_data.models import EnergyEntry
from django.utils import timezone

class Compliance(models.Model):
    compliance_id = models.AutoField(primary_key=True)
    factory = models.OneToOneField(Factory, on_delete=models.CASCADE)
    compliance_target = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    compliance_status = models.CharField(max_length=20, default='compliant', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_compliance_status(self, date=None):
        if date is None:
            date = timezone.now().date()
        tea_processed = EnergyEntry.get_tea_processed_sum_by_factory_and_date(self.factory.factory_id, date)
        co2_equivalent_sum = EnergyEntry.get_co2_sum_by_factory_and_date(self.factory.factory_id, date)
        emission_sum = Emissions.get_emission_sum_by_factory_and_date(self.factory.factory_id, date)
        total_emissions = co2_equivalent_sum + emission_sum
        
        co2_per_tea = total_emissions / tea_processed if tea_processed > 0 else 0
        
        if co2_per_tea > self.compliance_target or total_emissions > self.compliance_target:
            return 'non-compliant'
        else:
            return 'compliant'

    def save(self, *args, **kwargs):
        self.compliance_status = self.calculate_compliance_status()
        super().save(*args, **kwargs)
