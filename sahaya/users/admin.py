# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser  # Import your CustomUser model
from registration.models import Registration  # Import the Registration model from the events app
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin panel for users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'middle_initial', 'contact_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Define the fields to show when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'middle_initial', 'contact_number', 'email'),
        }),
    )

    # Set which fields to display in the list view in the Django admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

# Register the CustomUser model with the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)


