from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    middle_initial = models.CharField(max_length=1, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username
