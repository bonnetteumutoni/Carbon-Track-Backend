# from django.db import models

# class MCU(models.Model):
#     mcu_id = models.CharField(max_length=255, primary_key=True)  # Changed to CharField for string IDs; if AutoField, use models.AutoField(primary_key=True) but convert IDs to int
#     factory_id = models.ForeignKey('some_app.Factory', on_delete=models.CASCADE, null=True)  # Assuming a Factory model exists in another app; replace with actual
#     status = models.CharField(max_length=40, default='active')
#     created_at = models.DateTimeField(auto_now_add=True)  # Auto-sets to now on creation

#     def __str__(self):
#         return self.mcu_id
