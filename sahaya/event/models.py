from django.db import models
from django.contrib.auth.models import organizer

# Event Model
class Event(models.Model):
    event_id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    event_time = models.TimeField()
    organizer = models.ForeignKey(organizer, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
