from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import JsonResponse
from .models import Registration
from event.models import Event
from notification.models import Notification
import uuid

@login_required
def register_for_event(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        participant = request.user

        # Check if the user is already registered for this event
        registration, created = Registration.objects.get_or_create(
            event=event,
            participant=participant,
            defaults={
                "status": "Registered",
                "registration_date": timezone.now()
            }
        )

        if not created:
            return JsonResponse({"success": False, "error": "You are already registered for this event."})

        # Create a notification
        Notification.objects.create(
            notification_id=str(uuid.uuid4())[:10],
            notification_type="Event Registration",
            organizer=event.organizer,
            participant=participant,
            event=event
        )

        # Prepare email content
        subject = f"Registration Confirmation for {event.title}"
        html_message = render_to_string('notification/registration_email.html', {'event': event, 'participant': participant})
        plain_message = strip_tags(html_message)
        recipient_email = participant.email

        # Send the email
        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [recipient_email],
            html_message=html_message,
        )

        return JsonResponse({"success": True, "message": "Successfully registered for the event and email sent."})

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)
