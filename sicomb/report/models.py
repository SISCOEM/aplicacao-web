from django.db import models
from datetime import datetime
import pdfkit
from django.template.loader import render_to_string


class ReportManager(models.Manager):
    def get_report_fields(self, report):
        return Report_field.objects.filter(report=report)
    
    def generate_pdf(self, report):
        options = {
            'page-size': 'A4',
            'encoding': 'utf-8',  # Use a codificação UTF-8 para suportar acentos
        }
        
        pdf_str = render_to_string('report/pdf_template.html', {"report": report})
        
        pdf = pdfkit.from_file(pdf_str, False, options=options)
        return pdf

    
class Report(models.Model):
    type = models.CharField(max_length=256, default='', null=True, blank=True),
    title = models.CharField(max_length=256, default="Relatório %d/%m/%Y")
    date_creation = models.DateTimeField(default=datetime.now())

    objects = ReportManager()
    
    def __str__(self):
        return self.title


class Report_field(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    field = models.TextField(default=None, blank=True, null=True)
    content = models.TextField(default=None, blank=True, null=True)
    
    def __str__(self):
        return f"Campo: {self.field}, Conteúdo: {self.content}"
