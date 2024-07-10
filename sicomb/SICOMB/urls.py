import time
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .settings import AUX
from .main_view import main_view
from django.http import HttpResponse

def minha_view(request):
    dominio = request.META['HTTP_HOST']
    # Faça algo com o domínio, como verificar se corresponde a um domínio específico.

    return HttpResponse(f"Você está acessando o servidor com o domínio: {dominio}")


urlpatterns = [
    path('', main_view),
    path('admin/', admin.site.urls),
    path('equipamento/', include('equipment.urls')),
    path('carga/', include('load.urls')),
    path('police/', include('police.urls')),
    path('report/', include('report.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

