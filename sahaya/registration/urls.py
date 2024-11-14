# registration/urls.py
from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    path('register/<int:event_id>/', views.register_for_event, name='register'),  # Registration form URL
    

]