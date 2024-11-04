# notification/utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Notification
import uuid

def send_registration_email(event, participant):
    # Step 1: Create a notification entry
    Notification.objects.create(
        notification_id=str(uuid.uuid4())[:10],
        notification_type="Event Registration",
        organizer=event.organizer,
        participant=participant,
        event=event
    )

    # Step 2: Prepare email content
    subject = f"Registration Confirmation for {event.title}"
    html_message = render_to_string('notification/registration_email.html', {'event': event, 'participant': participant})
    plain_message = strip_tags(html_message)
    recipient_email = participant.email

    # Step 3: Send the email
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        html_message=html_message,
        fail_silently=False
    )
