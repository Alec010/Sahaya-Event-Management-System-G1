from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Registration
from event.models import Event
from django.utils import timezone

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
        messages.success(request, "Successfully registered for the event.")

    # Redirect to the dashboard in the users app
    return redirect("users:dashboard")  # Replace 'users:dashboard' with the actual name of your dashboard URL
