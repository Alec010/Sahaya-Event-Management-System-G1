from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page URL (landing page)
    path('signup/', views.signup_view, name='signup'),  # Sign-up page
    path('login/', views.login_view, name='login'),  # Login page
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard page
    path('logout/', views.logout_view, name='logout'),
]
