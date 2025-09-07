from rest_framework import serializers
from emissions.models import Emissions
from users.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from factory.models import Factory
from mcu.models import MCU
from emissions.models import Emissions
from energy_entry_data.models import EnergyEntry
from compliance_data.models import Compliance   
from users.models import User



class EmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emissions
        fields = "__all__"


from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from users.models import User
# Generic serializer to view/update user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }
# Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        error_messages={
            "min_length": "Password must be at least 8 characters long."
        },
    )
    phone_number = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Phone number already registered.")]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already registered.")]
    )
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password",
            "user_type",
            "factory",
        ]
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # hash password
        user.save()
        return user
    def validate(self, data):
        # Factory check for factory managers
        if data.get("user_type") == "factory" and not data.get("factory"):
            raise serializers.ValidationError("Factory is required for factory managers.")
        return data
# Login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials, please try again.")
        if not user.is_active:
            raise serializers.ValidationError("This account is disabled.")
        data["user"] = user
        return data

class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = '__all__'
        
class MCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCU
        fields = '__all__'
class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emissions
        fields = '__all__'
class EnergyEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyEntry
        fields = '__all__'
        read_only_fields = ['co2_equivalent']

class ComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compliance
        fields = '__all__'









