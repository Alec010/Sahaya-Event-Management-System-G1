from django.db import models
from django.contrib.auth.models import participant, event

# Registration Model
class Registration(models.Model):
    registration_id = models.CharField(max_length=10, primary_key=True)
    registration_date = models.DateTimeField()
    status = models.CharField(max_length=20)
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    participant = models.ForeignKey(participant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Registration {self.registration_id} for Event {self.event.title}"
