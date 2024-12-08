from django.urls import path
from . import views
from .views import export_report_pdf, report_page

app_name = 'report'  # This sets the namespace for the 'report' app

urlpatterns = [
    path('create_report/<int:event_id>/', views.create_report, name='create_report'),
    path('report/report_page/<int:event_id>/', report_page, name='report_page'),
    path('report/edit/<int:report_id>/', views.edit_report, name='edit_report'),
    path('report/delete/<int:report_id>/', views.delete_report, name='delete_report'),
    path('export_report_pdf/<int:report_id>/', export_report_pdf, name='export_report_pdf'),
]