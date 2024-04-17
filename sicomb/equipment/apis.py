import time
from django.shortcuts import render
from .models import *
from django.forms.models import model_to_dict
from django.http import JsonResponse
from SICOMB import settings
from load.models import *
from .templatetags.custom_filters import require_user_pass
from django.views.decorators.csrf import csrf_exempt
import simpleaudio as sa # usada para reprodução de um áudio

@csrf_exempt 
@require_user_pass
def get_bullets(request):
    """
    Descrição:
        Retorna todas as munições cadastradas no sistema fazendo a conversão da imagem para um link
    """
    bullets = Bullet.objects.all()
    data = {}
    for i, caliber in enumerate(bullets):
        data[i] = model_to_dict(caliber)
        data[i]['image_path'] = caliber.image_path.url if caliber.image_path else ''

    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


# valida o uid pra cadastro
@csrf_exempt
def valid_uid(request):
    """
    Descrição:
        Função que valida se o uid já está em algum equipamento com fins de verificar se pode ou não ser usado em um novo cadastro
    """

    if settings.AUX["uids"].__len__() > 0:
        uid = settings.AUX["uids"].pop()
        try:
            equipment = Equipment.objects.get(uid=uid)
            
            if not equipment.activated:
                return JsonResponse({"msm": "UID aguardando aprovação de um administrador!", "uid": ""}, json_dumps_params={'ensure_ascii': False})
                
        except Equipment.DoesNotExist:  # se não existe
            return JsonResponse(
                {"uid": uid},
                json_dumps_params={'ensure_ascii': False}
            )  # retorna o uid pq significa que pode cadastrar
        return JsonResponse({"msm": "UID já cadastrado", "uid": ""}, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({"uid": ""}, json_dumps_params={'ensure_ascii': False})


# valida o numero de série pra cadastro
@csrf_exempt
# @require_user_pass
def valid_serial_number(request, sn):
    """
    Descrição:
        Função que valida se o numero de série já está em algum equipamento com fins de verificar se pode ou não ser usado em um novo cadastro
    """
    try:
        equipment = Equipment.objects.get(serial_number=sn)
        
        if not equipment.activated:
            return JsonResponse({"msm": "Numero de série aguardando aprovação de um administrador!", "exists": True}, json_dumps_params={'ensure_ascii': False})

    except Equipment.DoesNotExist:  # se não existe
        return JsonResponse({"exists": False})  # retorna que não exist, json_dumps_params={'ensure_ascii': False}e
    return JsonResponse({"msm": "Numero de série já cadastrado", "exists": True}, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_user_pass
def get_equipment_serNum(request, serial_number):
    """
    Descrição da função:
        Retorna o equipamento pelo numero de série
    """

    print(serial_number)
    if "bullet::" not in serial_number: # 'bullet::' é um préfixo para diferenciar a munição dos demais modelos
        try:
            equipment = Equipment.objects.get(serial_number=serial_number)
            
            if not equipment.activated:
                return JsonResponse({"msm": "Equipamento aguardando aprovação de um administrador!", "registred": True, "uid": ""}, json_dumps_params={'ensure_ascii': False})
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"msm": "Equipamento não existe na base de dados!", "registred": False, "uid": ""}, 
                json_dumps_params={'ensure_ascii': False}
            )
        data = {
            "equipment": model_to_dict(equipment),
            "registred": equipment.model_type.model.replace("model_", ""), # registred é usada como uma chave com informações extras e usada a depender do contexto
            "model": model_to_dict(equipment.model),
        }
        data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else '' 
        # Converte a imagem

        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    elif "bullet::" in serial_number: # Se for uma munição
        serial_number = serial_number.replace("bullet::", "")
        try:
            bullet = Bullet.objects.get(caliber=serial_number)
            
            if not bullet.activated:
                return JsonResponse({"uid": "", "msm": "Munição aguardando aprovação de um administrador!", "registred": True}, json_dumps_params={'ensure_ascii': False})
            
        except Bullet.DoesNotExist:
            return JsonResponse(
                {
                    "msm": "Munição não existe na base de dados!",
                    "registred": False,
                    "uid": "",
                }, 
                json_dumps_params={'ensure_ascii': False}
            )
            
        data = {
            "uid": "Search",
            "model": model_to_dict(bullet),
            "registred": "bullet"
        }
        
        data['model']['image_path'] = bullet.image_path.url if bullet.image_path else ''
        data["equipment"] = data["model"]

        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


# @require_user_pass
@csrf_exempt
def get_tag(request):
    """
    Descrição:
        retorna o equipamento da tag passada
    """

    data = {
        "uid": ""
    }
    
    if len(settings.AUX["uids"]) > 0:
        uid = settings.AUX["uids"].pop()
        data["uid"] = uid
        
        try:
            equipment = Equipment.objects.get(uid=uid)
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"uid": uid}
            )
        
        data["equipment"] = model_to_dict(equipment)
        data["type"] = equipment.model_type.model.replace("model_", "")
        data["model"] = model_to_dict(equipment.model)
        data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''
        
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    
    
@csrf_exempt
@require_user_pass
def get_equipment_avalible(request):
    """
    Retorna o equipamento referente ao uid mais recente em formato JSON
    Especificamente diferente na questão de que, se ele estiver indisponível 
    ele retorna uma mensagem falando o motivo.
    
    Usado no processo de fetch load
    """
    
    data = {
        "uid": "",
        "confirmCargo": settings.AUX["confirm_cargo"],
    }

    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get("type") != None:
        # Caso seja uma munição
        if request.GET.get("type") == "bullet":
            caliber = request.GET.get("pk").replace("%20", " ")
            try:
                bullet = Bullet.objects.get(caliber=caliber)
                
                if not bullet.activated:
                    return JsonResponse({"uid": "", "msm": "Munição aguardando aprovação de um administrador!"}, json_dumps_params={'ensure_ascii': False})
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado", "a": caliber}, 
                    json_dumps_params={'ensure_ascii': False}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

            data = {
                "uid": "Search",
                "equipment": model_to_dict(bullet),
                "registred": "bullet",
            }
            data['equipment']['image_path'] = bullet.image_path.url if bullet.image_path else ''
            data['model'] = data['equipment']
        elif request.GET.get("type") == "equipment":
            try:
                equipment = Equipment.objects.get(serial_number=request.GET.get("pk"))
                
                if not equipment.activated:
                    return JsonResponse({"uid": "", "msm": "Equipamento aguardando aprovação de um administrador!"}, json_dumps_params={'ensure_ascii': False})
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}, 
                    json_dumps_params={'ensure_ascii': False}
                )
            data = {
                "uid": "Search",
                "equipment": model_to_dict(equipment),
                "registred": equipment.model_type.model.replace("model_", ""),
                "model": model_to_dict(equipment.model),
            }
            data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''

    # Para os equipamentos com a tag
    elif len(settings.AUX["uids"]) > 0:
        uid = settings.AUX["uids"].pop()
        data["uid"] = uid

        try:
            equipment = Equipment.objects.get(uid=uid)  # Recupera o objeto Equipamento
            
            if not equipment.activated:
                return JsonResponse({"uid": "", "msm": "Equipamento aguardando aprovação de um administrador!"}, json_dumps_params={'ensure_ascii': False})
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não cadastrado"}
            )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
        if equipment.status != "Disponível":
            return JsonResponse(
                {
                    "uid": "",
                    "msm": "Equipamento não disponível, equipamento em uma carga de "
                    + equipment.status,
                },
                json_dumps_params={'ensure_ascii': False}
            )

        data["equipment"] = model_to_dict(equipment)
        data["registred"] = equipment.model_type.model.replace("model_", "")
        data["model"] = model_to_dict(equipment.model)
        data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''

    return JsonResponse(data)  # Retorna o dicionário em forma de api, json_dumps_params={'ensure_ascii': False}


@csrf_exempt
@require_user_pass
def allow_cargo(request):
    """
    Descrição:
        Permite que a carga seja finalizada (Libera a opção)
    """

    settings.AUX["confirm_cargo"] = True
    return JsonResponse({})


@csrf_exempt
@require_user_pass
def get_equipment_unvalible(request, id):
    """
    Retorna o equipamento referente ao uid mais recente em formato JSON
    Especificamente diferente na questão de que, se ele estiver disponível 
    ele retorna uma mensagem falando o motivo.
    
    Usado no processo de fetch unload

    caso o equipamento passado tenha uma tag, e haja uma tag que foi passada no sensor, ele verifica se o equipamento da carga especificada está ou não disponível, caso não seja passado um calibre ou numero de serie ele checa se há uma tag  passada pela antena

    parametros:
        id: Id da carga em que o equipamento se encontra

    parametros por request.body
        type: Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag, então deve vir preenchido
        pk: numero de serie ou calibre

    """
    
    data = {
        "uid": "",
        "confirmCargo": settings.AUX["confirm_cargo"],
    }
    
    # Para caso o que o usuário esteja solicitando não seja algo que tenha uma tag
    if request.GET.get("type") != None:
        print(request.GET.get("pk"))
        data["registred"] = request.GET.get("type")

        # Caso seja uma munição
        if "bullet::" in request.GET.get("pk"):
            data["registred"] = "bullet"
            caliber = request.GET.get("pk").replace("bullet::", "")
            try:
                bullet = Bullet.objects.get(caliber=caliber)
                
                if not bullet.activated:
                    return JsonResponse({"uid": "", "msm": "Munição aguardando aprovação de um administrador!"}, json_dumps_params={'ensure_ascii': False})
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}, 
                    json_dumps_params={'ensure_ascii': False}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
            
            if Equipment_load.objects.filter(load=id, bullet=bullet).exists():
                data["uid"] = 'Search'
                data["equipment"] = model_to_dict(bullet)
                data["equipment"]['image_path'] = bullet.image_path.url if bullet.image_path else ''
                data["model"] = data["equipment"]
            else:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não presente na carga atual."}, 
                    json_dumps_params={'ensure_ascii': False}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora

        else:
            try:
                equipment = Equipment.objects.get(serial_number=request.GET.get("pk"))
                
                data["registred"] = equipment.model_type.model.replace("model_", ""),

                if not equipment.activated:
                    return JsonResponse({"msm": "UID aguardando aprovação de um administrador!", "uid": ""}, json_dumps_params={'ensure_ascii': False})
            except Equipment.DoesNotExist:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não cadastrado"}, 
                    json_dumps_params={'ensure_ascii': False}
                )
                
            if Equipment_load.objects.filter(load=id, equipment=equipment).exists():
                data = {
                    "uid": "Search",
                    "equipment": model_to_dict(equipment),
                    "registred": equipment.model_type.model.replace("model_", ""),
                    "model": model_to_dict(equipment.model),
                }
                data['model']['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''

                return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse(
                    {"uid": "", "msm": "Equipamento não presente na carga atual."}, 
                    json_dumps_params={'ensure_ascii': False}
                )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
                
                
    # Para os equipamentos com a tag
    elif settings.AUX["uids"].__len__() > 0: # cago haja uma tag q foi passada
        uid = settings.AUX["uids"].pop()
        data["uid"] = uid
        print(uid)

        try:
            equipment = Equipment.objects.get(uid=uid)  # Recupera o objeto Equipamento
            
            if not equipment.activated:
                return JsonResponse({"msm": "UID aguardando aprovação de um administrador!", "uid": ""}, json_dumps_params={'ensure_ascii': False})
        except Equipment.DoesNotExist:
            return JsonResponse(
                {"uid": "", "msm": "Equipamento não cadastrado"}, 
                json_dumps_params={'ensure_ascii': False}
            )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
        if equipment.status == "Disponível":
            return JsonResponse(
                {
                    "uid": "",
                    "msm": "Equipamento não está na carga.",
                }, 
                json_dumps_params={'ensure_ascii': False}
            )
        for equipment_load in Equipment_load.objects.filter(load=id):
            if equipment == equipment_load.equipment:
                data["equipment"] = model_to_dict(equipment)
                data["registred"] = equipment.model_type.model.replace("model_", "")
                data["model"] = model_to_dict(equipment.model)
                data["model"]['image_path'] = equipment.model.image_path.url if equipment.model.image_path else ''
                
                return JsonResponse(data)  # Retorna o dicionário em forma de ap, json_dumps_params={'ensure_ascii': False}i
                
        return JsonResponse(
            {"uid": "", "msm": "Equipamento não presente na carga atual."}, 
            json_dumps_params={'ensure_ascii': False}
        )  # Caso o equipamento não esteja cadastrado ele simplismente ignora
    return JsonResponse(data)  # Retorna o dicionário em forma de api, json_dumps_params={'ensure_ascii': False}


@csrf_exempt
# @require_user_pass
def set_uid(request):
    """
    Método que recebe o UID (da web) e armazena na memória
    """
    
    data = {"uid": "Não setado",
        "equipments": Equipment.objects.all()
    }
    
    if request.method == "GET":
        if (
            request.GET.get("uid") != ""
            and request.GET.get("uid") != None
            and request.GET.get("uid") not in settings.AUX["uids"]
        ):
            settings.AUX["uids"].append(request.GET.get("uid"))
            data["uid"] = settings.AUX["uids"][settings.AUX["uids"].__len__() - 1]
            
            som = sa.WaveObject.from_wave_file(settings.STATICFILES_DIRS[0] + "/sounds/passSound.wav")
            play_obj = som.play()
            play_obj.wait_done()
        
        print(settings.AUX["uids"])
    return render(request, "equipment/set_answer.html", data)
    

def set_uid_from_arduino():
    """
    Descrição da função:
    Esta função lê mensagens da porta serial da antena RFID e armazena os códigos UID recebidos em 'settings.AUX["uids"]'.

    """

    while True:
        linha = settings.AUX["messsage_serial_port"].readline().decode('utf-8').strip()

        print("printando linha")
        print(linha)
        
        time.sleep(200)
        
        # Armazena o UID recebido num array
        linha = linha.split("::")
        if linha[0] == "TAG_CODE":
            code = linha[1]
            if (
                code != ""
                and code != None
                and code not in settings.AUX["uids"]
            ):
                settings.AUX["uids"].append(code)
                settings.AUX["uids"][settings.AUX["uids"].__len__() - 1]
            print(settings.AUX["uids"])


@csrf_exempt
@require_user_pass
def get_uids(request):
    """
    Retorna:
        Array: JSON com todos os uids
    """
    
    dicionario = dict(enumerate(settings.AUX["uids"]))
    return JsonResponse(dicionario, json_dumps_params={'ensure_ascii': False})

