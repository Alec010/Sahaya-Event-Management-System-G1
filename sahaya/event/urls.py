from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('view/<int:event_id>/', views.view_event, name='view_event'),
    path('remove-participant/<int:event_id>/', views.remove_participant, name='remove_participant'),
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/', views.list_of_events, name='list_of_events'),
    path('<int:event_id>/cancel_registration/', views.cancel_registration, name='cancel_registration'),
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('calendar-events/', views.get_calendar_events, name='calendar-events'),
    path('calendar/', views.calendar_view, name='calendar'), 


]
