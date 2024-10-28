from django.db import models
from django.contrib.auth.models import User

# Participant Model
class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Participant: {self.user.first_name} {self.user.last_name}"
