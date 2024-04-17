from django.urls import path
from . import views

urlpatterns = [
    path("", views.filter_report, name='relatorios'),
    path("<int:id>/", views.get_report_page, name='relatorio'),
    path("get_pdf_file/<int:id>/", views.get_pdf_file, name='relatorio'),
]