from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'location',
            'start_date',
            'end_date',
            'event_time',
            'image'  # Include the image field
        ]
