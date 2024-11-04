from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('view/<int:event_id>/', views.view_event, name='view_event'),
    path("<int:event_id>/remove_participant/", views.remove_participant, name="remove_participant"),
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),


]
