
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from registration.models import Registration
from weasyprint import HTML
from .models import Report
from .forms import ReportForm
from event.models import Event  # Import Event model from the event app
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib import messages

def create_report(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        # Add the event to the POST data manually since it's disabled
        form_data = request.POST.copy()  # Make a copy of POST data
        form_data['event'] = event.id  # Explicitly set the event ID
        
        form = ReportForm(form_data)
        
        if form.is_valid():
            # Create and save the report, associating it with the event
            report = form.save(commit=False)
            report.event = event  # Associate the report with the event
            report.save()

            # After saving the report, update the event's status to 'finished'
            event.status = 'finished'
            event.save()

            # Redirect to the event list page
            return redirect('event:list_of_events')
        else:
            print(form.errors)  # Debugging any form errors
    else:
        # Prepopulate the form with the current event
        form = ReportForm(initial={'event': event})

    return render(request, 'report/create_report.html', {'form': form, 'event': event})


@login_required
def report_page(request, event_id):
    event = get_object_or_404(Event, pk=event_id)  # Get event based on event_id
    report = get_object_or_404(Report, event=event)  # Get the associated report for the event

    # Get the number of participants for the event
    num_participants = event.registration_set.count()  # Correctly count the number of participants

    # Check if the current user is the organizer or a participant
    is_organizer = request.user == event.organizer
    is_participant = Registration.objects.filter(event=event, participant=request.user).exists()

    context = {
        'report': report,
        'num_participants': num_participants,  # Correctly pass the participant count
        'is_organizer': is_organizer,
        'is_participant': is_participant,
        'event': event
    }

    return render(request, 'report/report_page.html', context)


def edit_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        # Process form data (assuming you're using Django forms or request.POST)
        report_type = request.POST.get('report_type')
        report_content = request.POST.get('report_content')

        # Update the report fields
        report.report_type = report_type
        report.report_content = report_content
        report.save()

        # Instead of returning JsonResponse, return a redirect to the report_page
        return redirect('report:report_page', event_id=report.event.id)

    return JsonResponse({
        'success': False,
        'message': 'Invalid request.',
    })

@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    event = report.event

    # Check if the user is the organizer of the event
    if request.user != event.organizer:
        return redirect('report:report_page', report_id=report.id)  # Redirect if not the organizer

    if request.method == 'POST':
        report.delete()
        return redirect('event:event_detail', event_id=event.id)  # Redirect to event page after deletion

    return render(request, 'report/delete_report.html', {'report': report})

@login_required
def export_report_pdf(request, report_id):
    # Retrieve the report based on the provided ID
    report = get_object_or_404(Report, id=report_id)
    event = report.event

    # Get the number of participants for the event
    num_participants = event.registration_set.count()

    # Prepare the context for the PDF (just exporting certain details)
    context = {
        'report': report,
        'event': event.title,
        'generated_at': report.generated_at,
        'report_type': report.report_type,
        'report_content': report.report_content,
        'num_participants': num_participants,
    }

    # Render the template to an HTML string (for PDF generation)
    html_content = render_to_string('report/export_report.html', context)

    # Generate the PDF from the HTML string
    pdf = HTML(string=html_content).write_pdf()

    # Create the HTTP response with the PDF file
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report_id}.pdf"'

    return response