from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse  # Import for handling AJAX responses
from .models import Event  # Import Event from the same app
from registration.models import Registration  # Import Registration from the registration app
from .forms import EventForm  # Import the EventForm (assuming you have created an EventForm)
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required
def register_for_event(request, event_id):
    # Get the event or show a 404 error if it doesn't exist
    event = get_object_or_404(Event, id=event_id)

    # Check if the logged-in user is the organizer of the event
    if event.organizer == request.user:
        messages.error(request, "You cannot register for your own event.")
        return redirect("event:view_event", event_id=event.id)  # Update the redirect URL name to 'view_event'

    # Check if the user has already registered for this event
    if Registration.objects.filter(event=event, participant=request.user).exists():
        messages.info(request, "You are already registered for this event.")
        return redirect("event:view_event", event_id=event.id)

    # Register the user for the event
    Registration.objects.create(
        registration_id=f"REG-{event.id}-{request.user.id}",  # Generate a unique registration ID
        event=event,
        participant=request.user,
        status="Registered"
    )
    
    messages.success(request, "Successfully registered for the event.")
    return redirect("event:view_event", event_id=event.id)

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)  # Add request.FILES to handle file uploads
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Automatically set the organizer as the logged-in user
            event.save()
            form.save_m2m()  # Save any ManyToMany relationships if needed

            # Check if the request is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                # If it's not an AJAX request, you might want to redirect as a fallback
                return redirect('event:success')
        else:
            # Return validation errors in case of form issues
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})
def view_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # Get the event by ID or show a 404 error if not found
    return render(request, 'event/view_event.html', {'event': event})  # Render the template with event data


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
            # Send form errors if the form is not valid
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
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    data = json.loads(request.body)
    participant_id = data.get("participant_id")

    # Ensure participant exists
    try:
        registration = Registration.objects.get(event=event, participant_id=participant_id)
        registration.delete()
        return JsonResponse({"success": True})
    except Registration.DoesNotExist:
        return JsonResponse({"success": False, "error": "Participant not found"})
@login_required
def list_of_events(request):
    # Get events organized by the logged-in user
    organized_events = Event.objects.filter(organizer=request.user)

    # Get events the user has registered for (participated in)
    participated_events = Event.objects.filter(registration__participant=request.user).distinct()

    return render(request, "event/list_of_events.html", {
        "organized_events": organized_events,
        "participated_events": participated_events,
    })
