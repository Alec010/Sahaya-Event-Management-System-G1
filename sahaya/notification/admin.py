from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser  # Your custom user model
from notification.models import Notification  # Import from the events app
admin.site.register(Notification)