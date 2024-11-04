"""
URL configuration for sahaya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views  # Import views from the users app
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Include the URLs for your users app
    path('', views.home_view, name='home'),  # Set the root URL to the home page
    path('event/', include('event.urls')),  # For event-related URLs
    path('registration/', include('registration.urls')),  # For registration-related URLs
    path('notification/', include('notification.urls')),  # For registration-related URLs
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

