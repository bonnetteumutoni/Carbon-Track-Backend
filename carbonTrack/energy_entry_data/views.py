from rest_framework import viewsets
from .models import EnergyEntryData
from .serializers import EnergyEntryDataSerializer
from rest_framework.permissions import IsAuthenticated

class EnergyEntryDataViewSet(viewsets.ModelViewSet):
    queryset = EnergyEntryData.objects.all()
    serializer_class = EnergyEntryDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optionally, filter to the logged-in user's entries
        user = self.request.user
        return EnergyEntryData.objects.filter(user=user)
    
    def perform_create(self, serializer):
        # Associate the logged-in user as the owner of the created entry
        serializer.save(user=self.request.user)
