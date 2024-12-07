from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'discover'

urlpatterns = [
    path('app/', views.app, name='app'),  # Changed to views.app
    path('add/', views.add_event, name='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),  # Edit Event
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),  # Delete Event
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)