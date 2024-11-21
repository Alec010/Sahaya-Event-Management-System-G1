from django.urls import path
from . import views

app_name = 'users'  # Set the app_name for namespacing

urlpatterns = [
    path('', views.home_view, name='home'),  
    path('signup/', views.signup_view, name='signup'),  
    path('login/', views.login_view, name='login'),  
    path('dashboard/', views.dashboard_view, name='dashboard'),  
    path('logout/', views.logout_view, name='logout'),
    path('account/edit/', views.edit_account, name='edit_account'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('account/', views.account_view, name='account'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),

]
