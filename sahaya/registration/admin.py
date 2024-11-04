from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser  # Your custom user model
from registration.models import Registration  # Import from the events app
admin.site.register(Registration)