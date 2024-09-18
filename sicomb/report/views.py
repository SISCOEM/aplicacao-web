from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
import pdfkit, os


def filter_report(request):
    data = {
        'reports': Report.objects.all(),
    }
    
    return render(request, 'report/filter-report.html', data)

def get_report_page(request, id):
    data = {
        'report': Report.objects.filter(id=id).first(),
        'fields': Report_field.objects.filter(report=id),
    } 
    return render(request, 'report/report.html', data)


def get_pdf_file(request, id):
    #return Report.objects.generate_pdf(Report.objects.filter(id=id).first())
    try:
        report = get_object_or_404(Report, id=id)
        pdf_path = report.generate_pdf()
        
        if not pdf_path or not os.path.exists(pdf_path):
            return HttpResponse("Erro ao gerar o relatório")
        
        
        with open(pdf_path, 'rb') as pdf:
            pdf = pdf.read()
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
            return response
        #response = HttpResponse(pdf, content_type='application/pdf')
        #response['Content-Disposition'] = f'attachment; filename="{report.title}.pdf"'
    except Report.DoesNotExist:
        return HttpResponse("Relatório inexistente")

