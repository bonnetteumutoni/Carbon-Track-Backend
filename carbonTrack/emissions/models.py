# from django.db import models
# from mcu.models import MCU  

# class Emissions(models.Model):
#     sensor_id = models.CharField(max_length=255, primary_key=True)  
#     mcu_id = models.ForeignKey(MCU, on_delete=models.CASCADE)
#     emission_rate = models.DecimalField(max_digits=10, decimal_places=6)  
#     updated_at = models.DateTimeField(auto_now=True) 

#     def __str__(self):
#         return f"{self.sensor_id} - {self.emission_rate}"