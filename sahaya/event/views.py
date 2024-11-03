from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import EventForm

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

@login_required
def success(request):
    return render(request, 'event/success.html')
