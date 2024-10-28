from django.db import models
from django.contrib.auth.models import User


# Organizer Model
class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Organizer: {self.user.first_name} {self.user.last_name}"
