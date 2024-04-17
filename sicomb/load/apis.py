import mimetypes
import os
import time
from django.forms import model_to_dict
from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import serial
from load.models import *
from equipment.models import *
from police.models import *
from django.conf import settings
from django.utils import timezone
from equipment.templatetags.custom_filters import require_user_pass


def check_load(request, id):
    """ Checa a carga, (fins de teste) """
    Load.objects.check_load(Load.objects.filter(id=id).first())
    return JsonResponse({})


def convert_date(data_hora_utc):
    """
    Converter para o fuso horário brasileiro
    """
    data_hora = timezone.datetime.strptime(data_hora_utc, "%Y-%m-%d %H:%M:%S.%f%z")
    data_hora_brasileira = data_hora.astimezone(timezone.get_current_timezone())
    formato_br = "%d/%m/%Y %H:%M:%S"
    data_hora_formatada = data_hora_brasileira.strftime(formato_br)

    return data_hora_formatada


@csrf_exempt
@require_user_pass
def get_loads_police(request, plate):
    """
    Retorna as cargas de acordo com a matrícula do policial
    """
    police = Police.objects.filter(matricula=plate).first()
    
    if police is None: 
        return JsonResponse({"message":"Policial não encontrado"}, json_dumps_params={'ensure_ascii': False})
    
    loads_filtrados = Load.objects.filter(police=police, 
        status__in=['ATRASADA', 'DENTRO DO PRAZO', 'DATA DE RETORNO NÃO DEFINIDA', 'PARCIALMENTE DESCARREGADA COM ATRASO', 'PARCIALMENTE DESCARREGADA']
    )
    
    # Criar uma lista chamada "loads" e preencher com os dicionários dos objetos load filtrados
    loads = []
    for load in loads_filtrados:
        dicionario_load = model_to_dict(load)
        dicionario_load["itens_amount"] = Equipment_load.objects.filter(
            load=load
        ).__len__()
        dicionario_load["date_load"] = convert_date(str(dicionario_load["date_load"]))
        if dicionario_load["expected_load_return_date"]:
            dicionario_load["expected_load_return_date"] = convert_date(
                str(dicionario_load["expected_load_return_date"])
            )

        loads.append(dicionario_load)

    data = {"loads_police": loads}

    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
@require_user_pass
def get_load(
    request, id
):  
    """
    Retorna uma resposta JSON com as informações de uma carga
    """
    
    tipo_model = {
        'wearable' : 'Vestimento',
        'accessory' : 'Acessório',
        'armament' : 'Armamento',
        'grenada' : 'Granada',
        'bullet' : 'Munição',
    }
    
    load = Load.objects.filter(id=id).first()
    if load is None: 
        return JsonResponse({"message":"Carga não encontrado"}, json_dumps_params={'ensure_ascii': False})
    
    equipment_loads = []
    for load_eq in Equipment_load.objects.filter(load=load, status="Pendente"):
        equipment_load = model_to_dict(load_eq)
        equipment = {
        }
        if load_eq.equipment:
            equipment["equipment"] = model_to_dict(load_eq.equipment)
            equipment["campo"] = tipo_model[load_eq.equipment.model_type.model.replace("model_", "")]
            equipment["model"] = model_to_dict(load_eq.equipment.model)
            equipment["model"]["image_path"] = load_eq.equipment.model.image_path.url if load_eq.equipment.model.image_path else ''
        else:
            equipment["equipment"] = model_to_dict(load_eq.bullet)
            equipment["equipment"]["image_path"] = load_eq.bullet.image_path.url if load_eq.bullet.image_path else ''
            equipment["model"] = equipment["equipment"]
            equipment["campo"] = "bullet"
            

        equipment["amount"] = load_eq.amount
        equipment_load["Equipment&model"] = equipment
        equipment_loads.append(equipment_load)

    load = model_to_dict(load)
    load["equipment_loads"] = equipment_loads

    return JsonResponse(load, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
@require_user_pass
def get_list_equipment_avalible(request):
    """
    Rota para obter a lista de equipamentos disponíveis pendentes no meio de uma carga, itens que já foram passados.
    Percorre a lista de equipamentos na sessão e verifica se cada equipamento está disponível.
    Se um equipamento não estiver disponível, limpa a lista de equipamentos.
    Retorna a lista de equipamentos disponíveis em formato JSON.
    """
    for i in settings.AUX["list_equipment"]:
        
        if "registred" in settings.AUX["list_equipment"][i] and settings.AUX["list_equipment"][i]["registred"] != "bullet":
            if Equipment.objects.get(serial_number=i).status.lower() != "disponivel":
                settings.AUX["list_equipment"] = {}
                
    return JsonResponse(settings.AUX["list_equipment"], json_dumps_params={'ensure_ascii': False})



# Retorna a lista com equipamentos passados
@csrf_exempt
@require_user_pass
def get_list_equipment(request):
    return JsonResponse(settings.AUX["list_equipment"], json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_user_pass
def get_info(request):
    """
    Retorna as informações do policial logado requisitando uma carga
    """

    data = {
        "matricula": settings.AUX['matricula'] if settings.AUX['matricula'] != '' else None,
    }
    
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_user_pass
def add_list_equipment(request):
    """
    Adiciona um equipamento na lista
    """

    # obs = request.POST.get('observation')
    serial_number = request.POST.get('serialNumber')
    amount = request.POST.get('amount')
    # serial_number = request.GET.get('serialNumber')
    # amount = request.GET.get('amount')
    
    print(serial_number)
    
    # if Police.objects.filter(username=user, password=password).exists():
    if "bullet::" not in serial_number:
        equipment = Equipment.objects.filter(serial_number=serial_number).first()
        
        if not equipment:
            return JsonResponse({"message": "Equipamento não encontrada!", "status": "error"}, json_dumps_params={'ensure_ascii': False})
        
        data = {
            "equipment": model_to_dict(equipment),
            "model": model_to_dict(equipment.model),
            "registred": equipment.model_type.model.replace("model_", ""),
            # "observation": obs if obs != "-" else "",
            "amount": amount,
        }
        
        data["model"]["image_path"] = equipment.model.image_path.url if equipment.model.image_path else ''
        
        settings.AUX["list_equipment"][serial_number] = data
        
    elif "bullet::" in serial_number:  # se for uma munição
        print("É uma munição!")
        bullet = Bullet.objects.filter(caliber=serial_number.replace("bullet::" ,"")).first()
        
        if not bullet:
            return JsonResponse({"message": "Munição não encontrada!", "status": "error"}, json_dumps_params={'ensure_ascii': False})
        
        if settings.AUX["list_equipment"].get(serial_number) is not None:
            print(settings.AUX["list_equipment"].get('serial_number'))
            settings.AUX["list_equipment"][serial_number]["amount"] += int(amount)
            
        else:
            data = {
                "model": model_to_dict(bullet),
                "campo": "Munição",
                # "observation": obs if obs != "-" else "",
                "amount": int(amount),
            }
            data["model"]["image_path"] = bullet.image_path.url if bullet.image_path else ''
            data["equipment"] = data["model"]
            settings.AUX["list_equipment"][serial_number] = data
    
    return JsonResponse({"uid": settings.AUX["list_equipment"]}, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_user_pass
def remove_list_equipment(request):
    """
    Remove um equipamento espeçífico da lista
    """

    serial_number = request.POST.get('serial_number')
    obs = request.POST.get('obs')
    settings.AUX["list_equipment_removed"][serial_number] = settings.AUX[
        "list_equipment"
    ][serial_number]
    
    settings.AUX["list_equipment_removed"][serial_number]["observation"] = obs if obs != "-" else ""
    del settings.AUX["list_equipment"][serial_number]  # deleta efetivamente

    return JsonResponse({"sucesso": "sucesso"}, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
@require_user_pass
def add_obs(request):
    """
    Adiciona uma observação ao equipamento
    """
    
    serial_number = request.POST.get('serialNumber')
    obs = request.POST.get('observation')
    id_cargo = request.POST.get('id_cargo')
    
    eq_loads = Load.objects.get(id=id_cargo).equipment_loads.all()
    
    if "bullet::" not in serial_number:
        for eq in eq_loads:
            if eq.equipment and eq.equipment.serial_number == serial_number:
                # eq.observation = obs
                # eq.status = "Justificado" # pode criar uma var no settings.AUX pra colocar os numeros de serie e as obs pra validar e salvar só qnd finalizar a carga
                # eq.save()
                data = {
                    "equipment": model_to_dict(eq.equipment),
                    "model": model_to_dict(eq.equipment.model),
                    "registred": eq.equipment.model_type.model.replace("model_", ""),
                    "observation": obs if obs != "-" else "",
                }
                
                data["model"]["image_path"] = eq.equipment.model.image_path.url if eq.equipment.model.image_path else ''
        
                settings.AUX["list_equipment"][serial_number] = {**data, **settings.AUX["list_equipment"][serial_number]}
                    
                settings.AUX["list_equipment_valid"] = True
                
                print("Sucesso salvando OBS")
                print(settings.AUX["list_equipment"])

                return JsonResponse({"sucesso": "sucesso"})

    elif "bullet::" in serial_number:  # se for uma munição
        for eq in eq_loads:
            if eq.bullet and eq.bullet.caliber == serial_number.replace("bullet::", ""):
                # eq.observation = obs
                # eq.status = "Justificado"
                
                # eq.save()
                data = {
                    "model": model_to_dict(eq.bullet),
                    "campo": "Munição",
                    "observation": obs if obs != "-" else "",
                }
                data["model"]["image_path"] = eq.bullet.image_path.url if eq.bullet.image_path else ''
                data["equipment"] = data["model"]
                settings.AUX["list_equipment"][serial_number] = {**data, **settings.AUX["list_equipment"][serial_number]}
                
                settings.AUX["list_equipment_valid"] = True
                
                print("Sucesso salvando OBS")
                print(settings.AUX["list_equipment"])
                
                return JsonResponse({"sucesso": "sucesso"})
        else:
            return JsonResponse({"Falha": "Falha"})
    else:
        return JsonResponse({"Falha": "Falha"})


@csrf_exempt
@require_user_pass
def send_load_relatory(request, id):
    """
    Envia o comprovante do relatório para o policial
    """
    load = Load.objects.filter(id=id).first()
    
    if not load:
        return JsonResponse({"status": False, "message": "Carga não encontrada!"})
    
    Load.objects.send_relatory(load)
    
    return JsonResponse({"status": True, "message": "Carga enviada com sucesso!"})


@csrf_exempt
@require_user_pass
def get_relatory(request, id):
    """
    Envia o comprovante do relatório para o adjunto logado
    """
    load = Load.objects.filter(id=id).first()
    
    if not load:
        return JsonResponse({"status": False, "message": "Carga não encontrada!"})
    
    Load.objects.send_relatory(load, to=request.user.email)
    
    return JsonResponse({"status": True, "message": "Carga enviada com sucesso!"})


@csrf_exempt
@require_user_pass
def reset_rfid(request):
    """
    Reseta a thread da antena do RFID caso de algum problema e trave
    """
    settings.AUX['restart_rfid_thread']()
    
    return JsonResponse({"status": True, "message": "Conexão resetada com sucesso!"})
    