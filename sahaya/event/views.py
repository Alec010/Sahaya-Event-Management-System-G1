from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse  # Import for handling AJAX responses
from .models import Event  # Import Event from the same app
from registration.models import Registration  # Import Registration from the registration app
from .forms import EventForm  # Import the EventForm (assuming you have created an EventForm)
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
import logging
from .models import Event
from registration.models import Registration
from notification.utils import send_registration_email


logger = logging.getLogger(__name__)

@login_required
@require_POST
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the logged-in user is the organizer of the event
    if event.organizer == request.user:
        return JsonResponse({"success": False, "error": "You cannot register for your own event."}, status=403)

    # Check if the user has already registered for this event
    if Registration.objects.filter(event=event, participant=request.user).exists():
        return JsonResponse({"success": False, "error": "You are already registered for this event."}, status=400)

    # Register the user for the event
    try:
        registration = Registration.objects.create(
            event=event,
            participant=request.user,
            status="Registered"
        )

        # If registration was successful, send an email
        send_registration_email(event, request.user)
        

        return JsonResponse({"success": True, "message": "Successfully registered for the event."})
    except Exception as e:
        # Catch unexpected errors and ensure a JSON response
        return JsonResponse({"success": False, "error": "An unexpected error occurred."}, status=500)
@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)  # Add request.FILES to handle file uploads
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Automatically set the organizer as the logged-in user
            event.save()
            form.save_m2m()  

            # Check if the request is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('event:success')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})



from django.http import JsonResponse

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure only the organizer can edit
    if event.organizer != request.user:
        return JsonResponse({"success": False, "error": "You are not allowed to edit this event."}, status=403)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})  # Return JSON response on success
        else:
            # Log errors to debug invalid form
            print("Form errors:", form.errors)
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    # If not a POST request, render the edit page (for when the user opens the modal)
    else:
        form = EventForm(instance=event)
        participants = Registration.objects.filter(event=event)
        return render(request, "event/edit_event.html", {
            "event": event,
            "form": form,
            "participants": participants
        })

@login_required
@require_POST
def remove_participant(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    try:
        # Parse the JSON request body
        data = json.loads(request.body)
        participant_id = data.get("participant_id")

        if not participant_id:
            logger.error("Participant ID missing from request.")
            return JsonResponse({"success": False, "error": "Participant ID is required."}, status=400)

        participant_id = int(participant_id)
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        logger.error("Invalid participant ID format: %s", e)
        return JsonResponse({"success": False, "error": "Invalid participant ID format."}, status=400)

    # Check if the logged-in user is the organizer of the event
    if event.organizer != request.user:
        logger.error("User is not the organizer and cannot remove participants.")
        return JsonResponse({"success": False, "error": "You are not allowed to remove participants from this event."}, status=403)

    # Attempt to find and delete the registration
    try:
        registration = Registration.objects.get(event=event, participant_id=participant_id)
        registration.delete()
        return JsonResponse({"success": True, "message": "Participant removed successfully."})
    except Registration.DoesNotExist:
        logger.error("Participant with ID %s not found for event %s.", participant_id, event_id)
        return JsonResponse({"success": False, "error": "Participant not found."}, status=404)
    except Exception as e:
        logger.error("Unexpected error occurred: %s", e)
        return JsonResponse({"success": False, "error": "An unexpected error occurred."}, status=500)
@login_required
def list_of_events(request):
    # Get events organized by the logged-in user, excluding finished events
    organized_events = Event.objects.filter(organizer=request.user).exclude(status='finished')

    # Get events the user has registered for (participated in), excluding finished events
    participated_events = Event.objects.filter(registration__participant=request.user).exclude(status='finished').distinct()

    # Get finished events (assuming 'status' is the field that tracks event status)
    finished_events = Event.objects.filter(status='finished')

    return render(request, "event/list_of_events.html", {
        "organized_events": organized_events,
        "participated_events": participated_events,
        "finished_events": finished_events,  # Add finished events to context
    })
@login_required
def view_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_registration = Registration.objects.filter(event=event, participant=request.user).first()
    
    context = {
        'event': event,
        'user_registered': bool(user_registration), 
        'registration': user_registration 
    }
    return render(request, 'event/view_event.html', context)

@login_required
@require_POST
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration = Registration.objects.filter(event=event, participant=request.user).first()

    if registration:
        registration.delete()
        return JsonResponse({"success": True, "message": "You have successfully canceled joining the event."})
    else:
        return JsonResponse({"success": False, "error": "You are not registered for this event."}, status=400)
@login_required
@require_POST
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    
    try:
        event.delete()
        return JsonResponse({"success": True, "message": "Event deleted successfully."})
    except Exception as e:
        return JsonResponse({"success": False, "error": "Failed to delete event."}, status=500)
    

@login_required
def get_calendar_events(request):
    organized_events = Event.objects.filter(organizer=request.user)
    participated_events = Event.objects.filter(registration__participant=request.user).distinct()

    events = []

    # Add organized events
    for event in organized_events:
        events.append({
            'id': event.id,
            'title': f"{event.title} (Organizer)",
            'start': f"{event.start_date}T{event.start_time}",
            'end': f"{event.end_date}T{event.end_time}",
            'allDay': False,
            'extendedProps': {
                'role': 'organizer',
                'description': event.description,
                'image': event.image.url if event.image else None,  # Add image URL if available
            }
        })

    # Add participated events
    for event in participated_events:
        events.append({
            'id': event.id,
            'title': f"{event.title} (Participant)",
            'start': f"{event.start_date}T{event.start_time}",
            'end': f"{event.end_date}T{event.end_time}",
            'allDay': False,
            'extendedProps': {
                'role': 'participant',
                'description': event.description,
                'image': event.image.url if event.image else None,  # Add image URL if available
            }
        })

    return JsonResponse(events, safe=False)


@login_required
def calendar_view(request):
    return render(request, 'event/calendar.html')