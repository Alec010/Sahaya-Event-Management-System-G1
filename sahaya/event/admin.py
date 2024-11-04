from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser  # Your custom user model
from event.models import Event  # Import from the events app
admin.site.register(Event)