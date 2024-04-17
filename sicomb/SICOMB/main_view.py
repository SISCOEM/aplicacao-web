import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import serial
from serial.tools import list_ports
from SICOMB.settings import AUX
from equipment.views import filter_equipment
from police.views import dashboard_police
from police.views import dashboard
from django.contrib.auth.models import Group
from django.contrib import messages

def error_page(request):
    return render(request, "error.html")

VIEW_POLICE = dashboard_police
VIEW_ADJUNCT = dashboard
VIEW_ADMIN = dashboard
VIEW_ERROR = error_page


@login_required
def main_view(request):
    if request.user.is_superuser:
        return VIEW_ADMIN(request)
    try:
        police_group = Group.objects.get(name="police")
        adjunct_group = Group.objects.get(name="adjunct")
        
        if police_group in request.user.groups.all():
            return VIEW_POLICE(request)
        elif adjunct_group in request.user.groups.all():
            return VIEW_ADJUNCT(request)
        else:
            print("O usuário não está presente em nenhum grupo de usuário!")
            messages.error(request, "O usuário não está presente em nenhum grupo de usuário! definindo como policial.")
            
            if len(request.user.groups.all()) == 0:
                request.user.groups.add(police_group)
            
            if police_group in request.user.groups.all():
                return VIEW_POLICE(request)
            else:
                return VIEW_ERROR(request)
            
    except Group.DoesNotExist:
        print("O usuário está presente em um grupo de usuário não existente!")
        messages.error(request, "O usuário está presente em um grupo de usuário não existente!")
        return VIEW_ERROR(request)

from .read_sensors import get_uids