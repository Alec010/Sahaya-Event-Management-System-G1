from django.db import models
from event.models import Event

class Report(models.Model):
    generated_at = models.DateTimeField()
    report_type = models.CharField(max_length=50)
    report_content = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report {self.id} for Event {self.event.title}"
