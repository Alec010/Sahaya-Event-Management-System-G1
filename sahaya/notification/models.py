from django.db import models
from django.contrib.auth.models import organizer,participant,event

# Notification Model
class Notification(models.Model):
    notification_id = models.CharField(max_length=10, primary_key=True)
    notification_type = models.CharField(max_length=30)
    sent_at = models.DateTimeField()
    organizer = models.ForeignKey(organizer, on_delete=models.CASCADE, null=True, blank=True)
    participant = models.ForeignKey(participant, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notification {self.notification_id}"