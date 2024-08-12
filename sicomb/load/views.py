from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from equipment.templatetags.custom_filters import has_group
from load.models import *
from equipment.models import *
from police.models import *
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .forms import *
from django.contrib import messages
from notifications_app_mobile.views import NotificationService

settings.AUX["list_equipment"] = {}  # lista de equipamentos
settings.AUX["list_equipment_removed"] = {}  # lista de equipamentos removidos


# cadastra a carga com a lista
@has_group('adjunct')
def read_qrcode(request):
    return render(request, 'load/read_qrcode.html')
    
@has_group('adjunct')
def confirm_load(request):
    """
    Rota principal para redirecionar à tela de carga/descarga e analizar o submit do formulário para efetivar a carga.

    TODO: Uma sugestão de melhoria seria quebrar em funções menores.
    """
    data = {
        "municoes": settings.AUX["calibres"]
    }
    police = None
    
    # Verifica se o método HTTP utilizado é POST e se a confirmação de carga está habilitada
    if request.method == "POST" and settings.AUX["confirm_cargo"]:
        # Limpa a matrícula e desativa a confirmação de carga
        settings.AUX["matricula"] = ''
        settings.AUX["confirm_cargo"] = False
        
        # Verifica se há equipamentos na lista ou na lista de equipamentos removidos
        if len(settings.AUX["list_equipment"]) > 0 or len(settings.AUX["list_equipment_removed"]) > 0:
            # Obtém o tipo de turno do formulário
            turn_type = request.POST.get("turn_type")
            data_hora_atual = datetime.now()  # pega a data atual
            turn_types = ['6H', '12H', '24H', '8H']

            # Calcula a data e hora futura baseada no tipo de turno
            if turn_type in turn_types:
                data_hora_futura = data_hora_atual + timedelta(
                    hours=int(turn_type.replace("H", ""))
                )
            else:
                data_hora_futura = None

            try:
                # Obtém informações do policial com base na placa
                police = Police.objects.get(matricula=request.POST.get("plate"))
            except Police.DoesNotExist:
                pass

            # Cria um objeto de carga no banco de dados
            load = Load(
                expected_load_return_date=data_hora_futura,
                turn_type=turn_type,
                police=police,
                adjunct=request.user,
                status="-",
            )
            load.save()
            
            # Adiciona tipos de turno extras
            turn_types += ['REQUISIÇÃO JUDICIAL', 'CONSERTO', 'INDETERMINADO']

            # Processa os equipamentos na lista de equipamentos
            if turn_type in turn_types:
                for key in settings.AUX["list_equipment"]:
                    
                    try:
                        observation = settings.AUX["list_equipment"][key]["observation"]
                    except:
                        observation = "-"
                        
                    # Verifica se o equipamento é uma munição
                    if "bullet::" not in key:
                        # Obtém o equipamento com base no número de série
                        equipment = Equipment.objects.get(serial_number=key)
                        # Atualiza o status do equipamento
                        equipment.status = turn_type
                        equipment.save()

                        # Salva a relação entre o equipamento e a carga no banco de dados
                        Equipment_load(
                            load=load,
                            equipment=equipment,
                            observation=observation,
                            amount=settings.AUX["list_equipment"][key]["amount"],
                        ).save()
                    elif "bullet::" in key:
                        # Obtém a munição com base no calibre
                        bullet = Bullet.objects.get(caliber=key.replace("bullet::", ''))
                        amount_to_subtract = int(settings.AUX["list_equipment"][key]["amount"])

                        # Atualiza a quantidade de munição disponível
                        if bullet.amount - amount_to_subtract < 0:
                            amount_to_subtract = bullet.amount
                            bullet.amount = 0
                            data["msm"] = "Munição insuficiente, munição zerada"
                        else:
                            bullet.amount -= amount_to_subtract

                        bullet.save()
                        
                        # Obtém ou cria uma relação entre a munição e a carga no banco de dados
                        equipment_load = Equipment_load.objects.filter(load=load, bullet=bullet).first()
                        
                        if equipment_load is not None:
                            equipment_load.amount = amount_to_subtract
                            equipment_load.save()
                        else:
                            Equipment_load(
                                load=load,
                                bullet=bullet,
                                observation=observation,
                                amount=amount_to_subtract,
                            ).save()
                            
                # Processa os equipamentos na lista de equipamentos removidos
                for key in settings.AUX["list_equipment_removed"]:
                    
                    try:
                        observation = settings.AUX["list_equipment_removed"][key]["observation"]
                    except:
                        observation = "-"
                    
                    if "bullet::" not in key:
                        equipment = Equipment.objects.get(serial_number=key)
                        equipment.status = turn_type
                        equipment.save()

                        Equipment_load(
                            load=load,
                            equipment=equipment,
                            observation=observation,
                            amount=settings.AUX["list_equipment_removed"][key]["amount"],
                            status="Pendente",
                        ).save()
                    elif "bullet::" in key:
                        bullet = Bullet.objects.get(caliber=key.replace("bullet::", ""))

                        Equipment_load(
                            load=load,
                            bullet=bullet,
                            observation=observation,
                            amount=settings.AUX["list_equipment_removed"][key]["amount"],
                            status="Pendente",
                        ).save()
                
                Load.objects.send_relatory(load)
                NotificationService().send_notification(
                    title="Nova carga",
                    message=f"Nova carga realizada por {request.user.name}",
                    data={"load_id": load.id},
                    expo_push_token=police.pushToken
                )

                # Limpa as variáveis de sessão
                settings.AUX["matricula"] = ""
                settings.AUX["list_equipment"].clear()
                settings.AUX["list_equipment_removed"].clear()
                
            # Processa a carga de descarga
            elif turn_type == "descarga":
                load.returned_load_date = datetime.now()
                load.status = "descarga"
                
                # Obtém a carga original para carga de descarga
                load_unload = Load.objects.filter(id=request.POST.get("load_id")).first()
                load.load_unload = load_unload
                load.save()
                
                # Obtém os equipamentos relacionados à carga original
                equipment_load_list = Equipment_load.objects.filter(load=load_unload)
                
                # Processa os equipamentos na lista de equipamentos
                for key in settings.AUX["list_equipment"]:
                    amount = int(settings.AUX["list_equipment"][key]["amount"])
                    
                    try:
                        observation = settings.AUX["list_equipment"][key]["observation"]
                    except:
                        observation = "-"
                    print(f"Observação do {key}: {observation}")
                    
                    if "bullet::" not in key:
                        equipment = Equipment.objects.get(serial_number=key)
                        equipment.status = "Disponível"
                        equipment.save()
                        
                        eq_load = equipment_load_list.filter(equipment=equipment).first()
                        
                        if observation != "-":
                            eq_load.status = "Justificado"
                        else:
                            eq_load.status = "Devolvido"
                            
                        eq_load.save()
                        
                        Equipment_load(
                            load=load,
                            equipment=equipment,
                            observation=observation,
                            amount=amount,
                            status="Devolvido",
                        ).save()
                        
                    elif "bullet::" in key:
                        bullet = Bullet.objects.get(caliber=key.replace("bullet::", ''))
                        bullet.amount += amount
                        bullet.save()
                        
                        equipment_load = Equipment_load.objects.filter(load=load_unload, bullet=bullet).first()
                        
                        if equipment_load is not None:
                            if equipment_load.amount - amount > 0:
                                equipment_load.amount -= amount
                                
                                Equipment_load(
                                    load=load_unload,
                                    bullet=bullet,
                                    amount=amount,
                                    status="Devolvido",
                                ).save()
                                
                                if observation != "-":
                                    equipment_load.status = "Justificado"
                                    equipment_load.observation = observation
                                
                                equipment_load.save()
                                
                            elif equipment_load.amount - amount < 0:
                                amount = equipment_load.amount
                                messages.error(request, "Quantidade incorreta! Munições totalmente devolvidas!")
                                equipment_load.status = "Devolvido"
                                equipment_load.save()
                                
                            else:
                                equipment_load.status = "Devolvido"
                                equipment_load.save()
                            
                            Equipment_load(
                                load=load,
                                bullet=bullet,
                                observation=observation,
                                amount=amount,
                                status="Devolvido",
                            ).save()
                        else:
                            messages.error(request, "Erro!")
                            
                load.save()
                
                Load.objects.send_relatory(load)
                
                settings.AUX["matricula"] = ""
                
                if load_unload: Load.objects.check_load(load_unload) 
                Load.objects.check_load(load)

                settings.AUX["list_equipment"].clear()
                settings.AUX["list_equipment_removed"].clear()
            else:
                messages.error(request, "Erro, Tipo do turno inválido!")
        elif settings.AUX["list_equipment_valid"]:
            settings.AUX["list_equipment_valid"] = False
            settings.AUX["list_equipment"].clear()
            settings.AUX["list_equipment_removed"].clear()
        elif settings.AUX["list_equipment_valid"]:
            pass
        else:
            messages.error(request, "Lista vazia!")

        data["policial"] = police
    
    Load.objects.check_all_loads()
        
    settings.AUX["matricula"] = ''
    return render(request, "load/load.html", data)



# Cancela a carga e zera as listas
@has_group('adjunct')
def cancel_load(request):
    """
    Reseta todas as variáveis da memória relacionado à carga
    """
    settings.AUX["confirm_cargo"] = False
    settings.AUX["list_equipment"].clear()
    settings.AUX["list_equipment_removed"].clear()
    return redirect("fazer_carga")


@has_group('adjunct')
def filter_loads(request):
    """
    filtra as cargas para a dashboard das cargas
    """
    queryset = Load.objects.all().exclude(turn_type="descarga")
    
    form = LoadFilterForm(request.GET)
    
    if form.is_valid():
        queryset = form.filter_queryset(queryset)
    
    loads = []
    for i in queryset:
        ec = Equipment_load.objects.filter(load=i)
        loads.append([i, len(ec)])
        
        Load.objects.check_load(i)
    
    context = {
        "loads": loads,
        "filter_form": form
    }
        
    return render(request, "load/filter-load.html", context)


@login_required
def get_carga_policial(request, pk):
    """
    Página da carga
    """
    load = get_object_or_404(Load, pk=pk)
    equipment_loads = load.equipment_loads.all()
    return render(request, "load/carga_policial.html", {'load': load, 'equipment_loads': equipment_loads})

