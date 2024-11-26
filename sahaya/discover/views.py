from django.shortcuts import render, redirect, get_object_or_404
from .models import Event

def app(request):
    # Fetch all events from the database
    events = Event.objects.all()
    return render(request, 'discover/app.html', {'events': events})

def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date_time = request.POST.get('date_time')
        description = request.POST.get('description')
        author = request.POST.get('author')
        link = request.POST.get('link')
        image = request.FILES.get('image')  # Handle uploaded image
        
        # Create the event
        event = Event.objects.create(
            title=title,
            date_time=date_time,
            description=description,
            author=author,
            link=link,
            image=image
        )
        return redirect('discover:app')  # Redirect to the app view after adding event

    return render(request, 'discover/add_link.html')

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)
        event.date_time = request.POST.get('date_time', event.date_time)
        event.description = request.POST.get('description', event.description)
        event.author = request.POST.get('author', event.author)
        event.link = request.POST.get('link', event.link)
        if 'image' in request.FILES:
            event.image = request.FILES['image']
        event.save()
        return redirect('discover:app')
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