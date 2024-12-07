from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from event.models import Event
from registration.models import Registration 
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')  # Redirect to the login page after successful sign-up
        else:
            # If the form is invalid, render the page with the errors
            return render(request, 'users/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:dashboard')  # Redirect to the dashboard after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def home_view(request):
    return render(request, 'users/home.html')  # Landing page

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')  # Dashboard page

@login_required
def account_view(request):
    return render(request, 'users/account.html')

def edit_account(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.contact_number = request.POST.get('contact_number')

        # Update password if provided
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)

        # Save the user instance
        user.save()

        # Add a unique success message
        messages.success(request, "Account successfully edited.")  
        return redirect('users:account')  

    return redirect('users:account')


@login_required
def delete_account(request):
    if request.method == 'POST' and request.POST.get('delete_account'):
        user = request.user
        logout(request)  
        user.delete()  
        messages.success(request, "Your account has been successfully deleted.")
        return redirect('users:home')  
    return render(request, 'users/profile.html')  

def logout_view(request):
    logout(request)
    return redirect('users:home')  

@login_required
def dashboard_view(request):
    # Fetch all events excluding finished events
    trending_events = Event.objects.exclude(status='finished')  

    # Fetch events the user is already registered for (excluding finished events)
    user_registered_events = Event.objects.filter(registration__participant=request.user).exclude(status='finished')

    context = {
        'trending_events': trending_events,
        'user_registered_events': user_registered_events,  
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']
        user = request.user
        user.profile_picture = profile_picture  
        user.save()  
        messages.success(request, 'Profile picture updated successfully!')
        return redirect('users:account')  
    else:
        messages.error(request, 'No file uploaded.')
        return redirect('users:account')
