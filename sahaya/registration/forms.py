# registration/forms.py
from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['status']  # Include other fields if necessary (e.g., registration-specific fields)

        widgets = {
            'status': forms.HiddenInput(),  # Default to "Registered" or similar if you wish
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = "Registered"
