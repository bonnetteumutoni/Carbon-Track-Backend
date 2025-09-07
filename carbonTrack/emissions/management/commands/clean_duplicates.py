# from django.core.management.base import BaseCommand
# from django.db.models import Count
# from emissions.models import Emissions 

# class Command(BaseCommand):
#     help = 'Remove duplicate Emissions by device_id, keep the newest only'

#     def handle(self, *args, **kwargs):
#         duplicates = Emissions.objects.values('device_id')\
#             .annotate(count=Count('emissions_id'))\
#             .filter(count__gt=1)

#         for dup in duplicates:
#             emissions_qs = Emissions.objects.filter(device_id=dup['device_id']).order_by('-updated_at')
#             emissions_qs.exclude(pk=emissions_qs.first().pk).delete()

#         self.stdout.write('Duplicates cleaned up successfully.')
