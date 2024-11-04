# registration/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from event.models import Event
from notification.utils import send_registration_email  # Import the utility function
from registration.models import Registration  # Make sure this is correctly imported

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the logged-in user is the organizer of the event
    if event.organizer == request.user:
        messages.error(request, "You cannot register for your own event.")
        return redirect("event:view_event", event_id=event.id)

    # Check if the user has already registered for this event
    registration, created = Registration.objects.get_or_create(
        event=event,
        participant=request.user,
        defaults={
            "status": "Registered",
            "registration_date": timezone.now()
        }
    )

    if not created:
        messages.info(request, "You are already registered for this event.")
    else:
        # If registration was successful, send an email
        send_registration_email(event, request.user)
        messages.success(request, "Successfully registered for the event and email sent.")

    # Redirect to the dashboard in the users app
    return redirect("users:dashboard")
