# notification/models.py

from django.db import models
from django.conf import settings
from event.models import Event

class Notification(models.Model):
    notification_id = models.CharField(max_length=10, primary_key=True)
    notification_type = models.CharField(max_length=30)
    sent_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_notifications"
    )
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_notifications"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.notification_type} - {self.event.title}"
