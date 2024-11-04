from django.db import models
from django.conf import settings

class Registration(models.Model):
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Registered")
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def formatted_registration_id(self):
        return f"REGISTRATION{self.id}"

    def __str__(self):
        return f"Registration {self.formatted_registration_id} for Event {self.event.title}"
