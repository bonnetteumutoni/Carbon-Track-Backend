from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'email',
            'password', 'user_type', 'factory_id', 'profile_image'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically adjust the factory_id field based on user_type
        if self.instance and self.instance.user_type == 'ktda_manager':
            self.fields.pop('factory_id')  # Remove factory_id field for KTDA managers
        else:
            self.fields['factory_id'].required = True  # Make factory_id required for factory managers

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        factory_id = cleaned_data.get('factory_id')

        # Validate factory_id based on user_type
        if user_type == 'factory_manager' and not factory_id:
            self.add_error('factory_id', 'Factory ID is required for Factory Managers.')
        if user_type == 'ktda_manager' and factory_id:
            self.add_error('factory_id', 'KTDA Managers cannot have a Factory ID.')

        return cleaned_data