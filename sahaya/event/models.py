from django.db import models
from django.conf import settings

class Event(models.Model):
    # Existing fields
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()  
    end_time = models.TimeField()   
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_events")
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    # New 'status' field with choices
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(
        max_length=8,  # 'active' and 'finished' both have 7 characters max
        choices=STATUS_CHOICES,
        default='active',  # Default to 'active'
        null=True,
        blank=True  # Make it optional, so the field can be empty
    )

    def __str__(self):
        return self.title

    def formatted_organizer_id(self):
        return f"Organizer_{self.organizer.username}"

    def get_participants(self):
        return [registration.participant for registration in self.registration_set.all()]
