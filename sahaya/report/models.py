from django.db import models
from django.contrib.auth.models import event

# Report Model
class Report(models.Model):
    report_id = models.CharField(max_length=10, primary_key=True)
    generated_at = models.DateTimeField()
    report_type = models.CharField(max_length=50)
    report_content = models.TextField()
    event = models.ForeignKey(event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report {self.report_id} for Event {self.event.title}"
