from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_date', 'end_date', 'start_time', 'end_time', 'image']

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get("location")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if location and start_date and start_time and end_time:
            # Check if an event already exists with the same location, overlapping date, and time
            overlapping_events = Event.objects.filter(
                location=location,
                start_date=start_date,
                start_time__lt=end_time,  # Starts before the new event's end time
                end_time__gt=start_time,  # Ends after the new event's start time
            )

            # If updating an event, exclude the current event from validation
            if self.instance and self.instance.pk:
                overlapping_events = overlapping_events.exclude(pk=self.instance.pk)

            if overlapping_events.exists():
                raise forms.ValidationError(
                    f"An event already exists at {location} on {start_date} from {start_time} to {end_time}."
                )

        return cleaned_data
