from django.db import models
from users.models import CustomUser  # Import the CustomUser model

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)  # Event title
    date_time = models.DateTimeField()  # Date and time of the event
    description = models.TextField()  # Event description
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')  # Foreign key to CustomUser
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)  # Event image
    link = models.URLField(blank=True, null=True)  # Event link
    categories = models.ManyToManyField('Category', blank=True)  # Categories related to the event
    

    def __str__(self):
        return self.title
