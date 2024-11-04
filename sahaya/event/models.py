# event/models.py
from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    event_time = models.TimeField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organized_events")
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def formatted_organizer_id(self):
        return f"Organizer_{self.organizer.username}"

    def get_participants(self):
        # Access related Registration objects without directly importing the Registration model
        return [registration.participant for registration in self.registration_set.all()]
