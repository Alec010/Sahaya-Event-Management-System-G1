import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone

def app(request):
    # Fetch all events from the database
    events = Event.objects.all()
    return render(request, 'discover/app.html', {'events': events})


from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event

@login_required
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        link = request.POST.get('link')
        image = request.FILES.get('image')  # Handle uploaded image
        
        # Set the date_time to the current date and time (automatically populated)
        date_time = timezone.now()  # Automatically set to the current server time

        # Get the currently logged-in user
        author = request.user  # This will be the CustomUser object of the logged-in user

        # Create the event and set the author to the logged-in user
        event = Event.objects.create(
            title=title,
            date_time=date_time,
            description=description,
            author=author,  # Set the user as the author (CustomUser object)
            link=link,
            image=image
        )
        return redirect('discover:app')  # Redirect to the app view after adding the event

    # Pass the current date and time to the template
    current_datetime = timezone.now()
    return render(request, 'discover/add_link.html', {'current_datetime': current_datetime})



from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from datetime import datetime

@login_required  # Ensure the user is logged in
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)

    # Keep the original event date_time without modification
    if request.method == 'POST':
        title = request.POST.get('title')
        date_time_str = request.POST.get('date_time')  # This will be ignored
        description = request.POST.get('description')
        link = request.POST.get('link')
        
        # Only update the fields you want to change (excluding date_time)
        image = request.FILES.get('image', event.image)  # Use the existing image if not updated

        # Set the author to the current logged-in user (CustomUser object)
        author = request.user  # Assuming request.user is a CustomUser instance

        # Update the event, but leave the original date_time unchanged
        event.title = title
        event.description = description
        event.author = author
        event.link = link
        event.image = image
        event.save()

        return redirect('discover:app')  # Redirect to the app view after editing the event

    return render(request, 'discover/edit_event.html', {'event': event})




def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('discover:app')
    
def app(request):
    search_term = request.GET.get('search', '')
    if search_term:
        events = Event.objects.filter(title__icontains=search_term)
    else:
        events = Event.objects.all()
    return render(request, 'discover/app.html', {'events': events})

def app(request):
    search_term = request.GET.get('search', '')  # Get search term from query parameters
    if search_term:
        events = Event.objects.filter(title__icontains=search_term)  # Case-insensitive search in title
    else:
        events = Event.objects.all()  # If no search term, show all events
    
    return render(request, 'discover/app.html', {'events': events})