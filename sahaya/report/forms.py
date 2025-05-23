from django import forms
from event.models import Event
from .models import Report

from django import forms
from .models import Report
from event.models import Event

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['generated_at', 'report_type', 'report_content', 'event']

        
    REPORT_TYPE_CHOICES = [
        ('completion', 'Completion Report'),
        ('summary', 'Summary Report'),
        ('feedback', 'Feedback Report'),
        ('performance', 'Performance Report'),
    ]

    # Use ChoiceField for report_type with the defined choices
    report_type = forms.ChoiceField(choices=REPORT_TYPE_CHOICES)

    generated_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    # Use ModelChoiceField to associate the Event
    event = forms.ModelChoiceField(queryset=Event.objects.all(), widget=forms.Select(attrs={'disabled': 'disabled'}))

    def __init__(self, *args, **kwargs):
        event = kwargs.get('initial', {}).get('event', None)
        super().__init__(*args, **kwargs)
        if event:
            # Pre-fill the event field and make it readonly
            self.fields['event'].initial = event
            self.fields['event'].queryset = Event.objects.filter(id=event.id)

       # Disable the 'generated_at' field (making it read-only)
        self.fields['generated_at'].widget.attrs['disabled'] = 'disabled'
