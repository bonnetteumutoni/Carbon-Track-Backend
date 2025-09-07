from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,viewsets, generics
from emissions.models import Emissions
from .serializers import EmissionsSerializer, RegisterSerializer, LoginSerializer
from django.utils import timezone
from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.utils.dateparse import parse_date
from api.serializers import FactorySerializer, UserSerializer, MCUSerializer, EmissionSerializer, EnergyEntrySerializer, ComplianceSerializer
from factory.models import Factory
from mcu.models import MCU
from emissions.models import Emissions
from energy_entry_data.models import EnergyEntry
from compliance_data.models import Compliance
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404



class EmissionsViewSet(viewsets.ModelViewSet):
    queryset = Emissions.objects.all().order_by('-updated_at') 
    serializer_class = EmissionsSerializer

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Invalid phone number or password.'}, status=status.HTTP_401_UNAUTHORIZED)

            if user.check_password(password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_type': user.type}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid phone number or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    



class FactoryViewSet(viewsets.ModelViewSet):
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer
    # permission_classes = [permissions.IsAuthenticated]



# Register new user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
# Login user
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
# List all users (optional, can restrict to admins)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
# Get, update, delete single user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class MCUViewSet(viewsets.ModelViewSet):
    queryset = MCU.objects.all()
    serializer_class = MCUSerializer

    def create(self, request, *args, **kwargs):
        mcu_id = request.data.get('mcu_id')
        # Check if MCU with mcu_id exists, else return 404 error
        mcu = get_object_or_404(MCU, pk=mcu_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(mcu=mcu)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # permission_classes = [permissions.IsAuthenticated]

class EmissionViewSet(viewsets.ModelViewSet):
    queryset = Emissions.objects.all()
    serializer_class = EmissionSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def sum_by_factory_and_date(self, request):
        factory_id = request.query_params.get('factory_id')
        date_str = request.query_params.get('date')
        date = parse_date(date_str) if date_str else timezone.now().date()
        total = Emissions.get_emission_sum_by_factory_and_date(factory_id, date)
        return Response({'factory_id': factory_id, 'date': date, 'total_emission': total})
    
class EnergyEntryViewSet(viewsets.ModelViewSet):
    queryset = EnergyEntry.objects.all()
    serializer_class = EnergyEntrySerializer
    # permission_classes = [permissions.IsAuthenticated]
    @action(detail=False, methods=['get'])
    def summation_by_factory_and_date(self, request):
        factory_id = request.query_params.get('factory_id')
        date_str = request.query_params.get('date')
        date = parse_date(date_str) if date_str else timezone.now().date()
        co2 = EnergyEntry.get_co2_sum_by_factory_and_date(factory_id, date)
        tea_processed = EnergyEntry.get_tea_processed_sum_by_factory_and_date(factory_id, date)
        return Response({'factory_id': factory_id, 'date': date, 'co2_sum': co2, 'tea_processed_sum': tea_processed})
    
class ComplianceViewSet(viewsets.ModelViewSet):
    queryset = Compliance.objects.all()
    serializer_class = ComplianceSerializer
    # permission_classes = [permissions.IsAuthenticated]
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        compliance = self.get_object()
        date_str = request.data.get('date')
        date = parse_date(date_str) if date_str else timezone.now().date()
        compliance.update_compliance(date)
        serializer = self.get_serializer(compliance)
        return Response(serializer.data)



















