from django.shortcuts import render
from .models import WireData
from django.http import JsonResponse
from django.utils import timezone
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required





# Create your views here.
def api_view(request):
    level = request.GET.get('level', None)

    if level is not None:
        # Convert level to float
        level = float(level)

        # Create a dictionary to store the data you want to save
        data_to_save = {
            'datetime': timezone.now(),
            'level': level,
        }

        # Create a new entry in the database using the data
        WireData.objects.create(**data_to_save)

        return JsonResponse({"message": "Data saved successfully"})
    else:
        return JsonResponse({"error": "Level parameter is required"}, status=400)







@login_required
def overall_view(request):
    wire_data = WireData.objects.all()
    return render(request, 'wireapp/overall.html', {'wire_data': wire_data})

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf_report(request):
    # Assuming you have Django models for each category
    wire_data = WireData.objects.all()

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="System_report.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    def draw_section(title, data, y_start):
        p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(300, y_start, title)

        p.setFont("Helvetica", 12)
        p.drawCentredString(300, y_start - 20, "-" * 50)

        records_per_page = 25
        for i, item in enumerate(data):
            # Calculate the starting y coordinate for each record
            record_y_start = y_start - 40 - (i % records_per_page) * 20

            # Start a new page for each section or after 25 records
            if i % records_per_page == 0 and i != 0:
                p.showPage()
                p.setFont("Helvetica-Bold", 18)
                p.drawCentredString(300, 770, f"{title} (continued)")
                p.setFont("Helvetica", 12)
                y_start = 780  # Reset y_start for the new page

            p.drawString(70, record_y_start, f"Record {i + 1}: {item.timestamp}, {item.level}, {item.status}")

    # Set an initial y_start value
    draw_section("Level System Data", wire_data, 770)

    # Save the PDF
    p.showPage()
    p.save()

    return response





def generate_chart_data_report_view(request):
    sensor_data = WireData.objects.all()
    pdf_response = generate_pdf_report(sensor_data)
    return pdf_response
