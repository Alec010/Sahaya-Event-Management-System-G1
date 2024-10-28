from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            return redirect('login')  # Redirect to the login page after successful sign-up
        else:
            print("Form is not valid")
            print(form.errors)  # Log errors to console
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
                return redirect('dashboard')  # Redirect to the dashboard after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def home_view(request):
    return render(request, 'users/home.html')  # Landing page

def dashboard_view(request):
    return render(request, 'users/dashboard.html')  # Dashboard page

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logging out
