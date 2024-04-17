from django.shortcuts import render
from .models import *
import pdfkit


def filter_report(request):
    data = {
        'reports': Report.objects.all(),
    }
    
    return render(request, 'report/filter-report.html', data)

def get_report_page(request, id):
    data = {
        'report': Report.objects.filter(id=id).first(),
    }
    
    return render(request, 'report/report.html', data)


def get_pdf_file(request, id):
    return Report.objects.generate_pdf(Report.objects.filter(id=id).first())

