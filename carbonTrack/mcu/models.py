from django.db import models
from factory.models import Factory

class MCU(models.Model):
    mcu_id = models.CharField(max_length=255, primary_key=True)
    factory = models.OneToOneField(Factory, on_delete=models.CASCADE, related_name='mcu', null=True)
    status = models.CharField(max_length=40, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def assign_factory_based_on_mcu_id(mcu_id):
        if mcu_id.startswith('ESP32-') and all(c == '0' for c in mcu_id[6:]):
            return Factory.objects.get(factory_id=67)
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.factory_id:
            assigned_factory = self.assign_factory_based_on_mcu_id(self.mcu_id)
            if assigned_factory:
                self.factory = assigned_factory
                
        if self.pk:
            original = MCU.objects.get(pk=self.pk)
            if original.factory_id and original.factory_id != self.factory_id:
                raise ValueError("Cannot change factory once MCU assigned")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.mcu_id
