import json
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from equipment.models import Equipment
from equipment.templatetags.custom_filters import has_group
from police.forms import PoliceFilterForm, PoliceForm
from django.contrib.auth.decorators import login_required
from .models import *
from load.models import Load, Equipment_load
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from cryptography.fernet import Fernet
from django.db.models import Q
from rest_framework.response import Response
from .serializers import RequestLoad
from load.forms import LoadFilterForm

# @login_required # Talvez seja necessário descomentar
def login(request):
    """
    View para processar o login de um policial com o fim de requisitar uma carga.
    Verifica as informações de login fornecidas no formulário.
    Se o login for bem-sucedido, define a matrícula do usuário na sessão.
    Retorna a página de solicitação de carga com informações do usuário e cargas recentes.
    """
    data = {}
    settings.AUX["matricula"] = ''
    
    if settings.AUX.get("matricula"):
        return redirect('destino')
    
    if request.method == "POST":
        body = {}
        try:
            body = json.loads(request.body)
        except Exception as error:
            pass
        # Verifica se não foi o botão de cancelar que foi pressionado
        if not request.POST.get("cancelar"):
            # Verifica o tipo de login (senha ou impressão digital)
            if request.POST.get("type_login") == "password":
                try:
                    police = Police.objects.get(
                        matricula=request.POST.get("matricula")
                    )
                    
                except Police.DoesNotExist:
                    messages.error(request, "Matrícula incorreta!")
                    return render(
                        request, "police/request_cargo.html"
                    )
                
                # Verifica se a senha fornecida é correta
                if check_password(request.POST.get("senha"), police.password):
                    if not police.activated or police.activator is None:
                        messages.error(request, "Policial aguardando aprovação de um administrador!")
                        
                        return render(request, "police/request_cargo.html", data)
                    
                    # Desativa a confirmação de carga
                    settings.AUX["confirm_cargo"] = False
                    # Define a matrícula do policial na sessão
                    settings.AUX["matricula"] = request.POST.get("matricula")

                    # Adiciona informações do policial e suas cargas recentes aos dados a serem renderizados
                    data["police"] = police
                    loads = Load.objects.filter(police=police).order_by('-date_load')[:35]
                    data["loads"] = []
                    for i in loads:
                        ec = Equipment_load.objects.filter(load=i)
                        data["loads"].append([i, len(ec)])
                else:
                    messages.error(request, "Senha incorreta!")
                    
            if request.POST.get("type_login") == "fingerprint": # Login via impressão digital
                
                if request.POST.get("token"):
                    police = None
                    
                    try:
                        # Decodifica o token de acesso usando a chave configurada
                        fernet = Fernet(settings.AUX["key_token_login_police"])
                        info = fernet.decrypt(request.POST.get("token").encode()).decode('utf-8').split("::")
                        print(info)
                        police = Police.objects.filter(matricula=info[1]).first()
                    except:
                        pass
                    
                    if police is not None:
                        # Limpa a chave de token de acesso
                        settings.AUX["key_token_login_police"] = None
                        
                        if not police.activated:
                            messages.error(request, "Policial aguardando aprovação de um administrador!")
                            
                            return render(request, "police/request_cargo.html", data)
                        
                        # Desativa a confirmação de carga
                        settings.AUX["confirm_cargo"] = False
                        # Define a matrícula do policial na sessão
                        settings.AUX["matricula"] = police.matricula

                        # Adiciona informações do policial e suas cargas recentes aos dados a serem renderizados
                        data["police"] = police
                        loads = Load.objects.filter(police=police).order_by('-date_load')[:35]
                        data["loads"] = []
                        
                        for i in loads:
                            ec = Equipment_load.objects.filter(load=i)
                            data["loads"].append([i, len(ec)])
                else:
                    # Retorna uma mensagem de erro se o token de acesso estiver ausente
                    messages.error(request, "Token de acesso inexistente!")
            try:
                if body['type_login'] == "app":
                    try:
                        police = Police.objects.get(
                            matricula=body['matricula']
                        )
                        settings.AUX["confirm_cargo"] = False
                        settings.AUX["matricula"] = body['matricula']
                        data["police"] = police
                        loads = Load.objects.filter(police=police).order_by('-date_load')[:35]
                        data["loads"] = []
                        for i in loads:
                            ec = Equipment_load.objects.filter(load=i)
                            data["loads"].append([i, len(ec)])
                    except Police.DoesNotExist:
                        return Response({"error": "Não foi possível encontrar policial!"})
            except Exception as error:
                pass

    
    # Renderiza a página de solicitação de carga com os dados apropriados
    return render(request, "police/request_cargo.html", data)


def destino(request):
    data = {}

    # Tente obter a matrícula do policial da sessão
    matricula = settings.AUX.get("matricula")
    
    if not matricula:
        return redirect('request_cargo_login')  # Redireciona para a página de login se não estiver logado

    try:
        # Busca o policial com base na matrícula da sessão
        police = Police.objects.get(matricula=matricula)
        settings.AUX["confirm_cargo"] = False  # Desativa a confirmação de carga
        data["police"] = police  # Adiciona o policial aos dados a serem renderizados

        # Busca as cargas recentes do policial
        loads = Load.objects.filter(police=police).order_by('-date_load')[:35]
        data["loads"] = []
        for load in loads:
            ec = Equipment_load.objects.filter(load=load)
            data["loads"].append([load, len(ec)])  # Adiciona a carga e a contagem de equipamentos
            
    except Police.DoesNotExist:
        return Response({"error": "Não foi possível encontrar policial!"})

    # Renderiza a página de solicitação de carga com os dados apropriados
    return render(request, "police/requesting_cargo.html", data)




@has_group('adjunct')
def register_police(request):
    """
    View para registrar um novo policial.
    Processa o formulário de registro de policiais.
    Retorna uma mensagem de sucesso se o registro for bem-sucedido.
    """
    if request.method == "POST":
        form = PoliceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, "Cadastro realizado com sucesso!")
            return HttpResponseRedirect("/police/register/")
        else:
            print("Invalido")
    else:
        form = PoliceForm()

    return render(
        request,
        "police/forms.html",
        context={
            "form": form,
        },
    )


@has_group('adjunct')
def search_police(request, id):
    """
    View para pesquisar um policial por ID.
    Verifica se o policial existe e, se existir, permite a edição de suas informações.
    """
    try:
        police = Police.objects.only("id").get(id=id)
    except Police.DoesNotExist:
        police = None
        messages.error(request, "Policial não encontrado!")
        return HttpResponseRedirect("/police/register/")

    if request.method == "POST":
        form = PoliceForm(request.POST, request.FILES, instance=police)
        
        if form.is_valid():
            police = form.save()
            
            group_police, _ = Group.objects.get_or_create(name='police')

            if not police.groups.filter(name='police').exists():
                police.groups.add(group_police)
            
            messages.success(request, "Atualização realizada com sucesso!")
            return HttpResponseRedirect("/police/filter/")
    else:
        form = PoliceForm(instance=police)

    return render(
        request,
        "police/forms.html",
        context={
            "police": police,
            "form": form,
            "edit": True
        },
    )


@login_required
def dashboard_police(request):
    """
    View do painel de controle do policial.
    Retorna informações sobre as cargas do policial.
    """
    police = Police.objects.filter(police=request.user).first()
    
    if police is None:
        messages.error(request, "Policial não encontrado!")
        return render(request, "error.html")
    
    form = LoadFilterForm(request.GET)
    
    loads = Load.objects.filter(police=request.user).order_by('-date_load')
    
    if form.is_valid():
        loads = form.filter_queryset(loads)
        
        
    context = {
        'cargos' : '',
        "loads": [],
        'filter_form': form
    }
    
    for i in loads:
        ec = Equipment_load.objects.filter(load=i)
        context["loads"].append([i, len(ec)])
    return render(request, "police/police_page.html", context)


@login_required
def perfil_police(request, id):
    """
    View do perfil de um policial.
    Retorna informações sobre as cargas associadas ao policial.
    """
    police = Police.objects.filter(id=id).first()
    
    if police is None:
        messages.error(request, "Policial não encontrado!")
        return render(request, "error.html")
    
    form = LoadFilterForm(request.GET)
    
    loads = Load.objects.filter(adjunct=police) | Load.objects.filter(police=police)
    
    if form.is_valid():
        loads = form.filter_queryset(loads)
        
    context = {
        'cargos' : '',
        "loads": [],
        'police': police,
        'filter_form': form
    }
    
    for i in loads:
        ec = Equipment_load.objects.filter(load=i)
        context["loads"].append([i, len(ec)])
        
    return render(request, "police/police_perfil.html", context)

@has_group('admin')
def promote_police(request):
    """
    View para promover um policial de "police" para "adjunct".
    """
    group, created = Group.objects.get_or_create(name='police')
    police_list = Police.objects.filter(groups=group, activated=True).exclude(activator=None)
    filter_form = PoliceFilterForm(request.GET)
    
    if filter_form.is_valid():
        police_list = filter_form.filter_queryset(police_list)
    
    context = {
        "btn_promote": "PROMOVER",
        "police_list": police_list,
        'filter_form': filter_form,
    }
    
    if request.method == 'POST':
        print(request.POST)
        id = request.POST.get("pk")
        try:
            police = Police.objects.get(pk=id)
            police.tipo = "Adjunto"
            police.save()
            
            police.groups.remove(group)
            group_adjunct, created = Group.objects.get_or_create(name='adjunct')
            police.groups.add(group_adjunct)
            
            context["msm"] = "Promovido com sucesso!"
            return render(request, 'police/manage_police.html', context)
        except:
            context["msm"] = "Falha, já existe um adjunto com esse nome!"
            return render(request, 'police/manage_police.html', context)
        
    return render(request, 'police/manage_police.html', context)


def ler_settings():
    """
    Função para ler as configurações do arquivo settings.json.
    """
    caminho_arquivo = os.path.join(settings.STATICFILES_DIRS[0], 'json', 'settings.json')
    
    sett = None
    
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            sett = json.load(arquivo)

    except FileNotFoundError:
        print("Arquivo não encontrado")

    except Exception as e:
        print(f"Erro ao ler o arquivo: {str(e)}")
    
    return sett


def escrever_settings(dados):
    """
    Função para escrever as configurações no arquivo settings.json.
    """
    caminho_arquivo = os.path.join(settings.STATICFILES_DIRS[0], 'json', 'settings.json')
    
    try:
        with open(caminho_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

    except Exception as e:
        print(f"Erro ao escrever no arquivo: {str(e)}")


@has_group('admin')
def settings_view(request):
    """
    TODO: View para visualizar e editar as configurações do sistema.
    """
    sett = ler_settings()
    
    if request.method == 'POST':
        key = request.POST.get('key')
        value = request.POST.get('value')
        
        sett[key] = value
        
        escrever_settings(sett)
    
    context = {
        "settings": settings.AUX,
    }
        
    return render(request, 'police/admin/settings.html', context)


@has_group('admin')
def reduce_police(request):
    """
    View para rebaixar um policial de "adjunct" para "police".
    """
    group, created = Group.objects.get_or_create(name='adjunct')
    police_list = Police.objects.filter(groups=group, activated=True).exclude(activator=None)
    filter_form = PoliceFilterForm(request.GET)
    
    if filter_form.is_valid():
        police_list = filter_form.filter_queryset(police_list)
    
    context = {
        "btn_promote": "REBAIXAR",
        "police_list": police_list,
        'filter_form': filter_form,
    }

    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            police = Police.objects.get(pk=id)
            police.tipo = "Policial"
            police.save()
            
            police.groups.remove(group)
            group_police, _ = Group.objects.get_or_create(name='police')

            police.groups.add(group_police)
            
        except Police.DoesNotExist:
            context["msm"] = "Falha, o policial não foi encontrado!"
            return render(request, 'police/reduce_police.html', context)

    return render(request, 'police/manage_police.html', context)


@has_group('admin')
def approve_police(request):
    """
    View para aprovar ou desaprovar solicitações de registro de policiais.
    """
    police_list = Police.objects.filter(Q(activated=False) | Q(activator=None))
    filter_form = PoliceFilterForm(request.GET)
    
    if filter_form.is_valid():
        police_list = filter_form.filter_queryset(police_list)
    
    context = {
        "btn_promote": "APROVAR",
        "police_list": police_list,
        'filter_form': filter_form,
    }
    
    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            police = Police.objects.get(pk=id)
            
            police.activator = request.user
        
            action = request.POST.get("action-type")
            if action:
                if action == 'approve':
                    police.activated = 1
                    police.save()
                elif action == 'disapprove':
                    police.delete()
            
            else:
                messages.error(request, "Falha, ação indefinida!")
            
        except Police.DoesNotExist:
            messages.error(request, "Falha, o policial não foi encontrado!")
            
            return render(request, 'police/reduce_police.html', context)

    return render(request, 'police/manage_police.html', context)


@has_group('adjunct')
def filter_police(request):
    """
    View para filtrar e visualizar policiais.
    """
    police_list = Police.objects.filter(activated=True).exclude(activator=None)
    filter_form = PoliceFilterForm(request.GET)
    
    if request.method == 'POST':
        id = request.POST.get("pk")
        try:
            request.method = "GET"
            
            return HttpResponseRedirect("/police/search/" + id + "/")
        except Police.DoesNotExist:
            messages.error(request, "Falha, o policial não foi encontrado!")
            
            return render(request, 'police/reduce_police.html', context)
    
    if filter_form.is_valid():
        police_list = filter_form.filter_queryset(police_list)
    
    context = {
        "btn_promote": "EDITAR",
        'police_list': police_list,
        'filter_form': filter_form,
    }

    return render(request, 'police/manage_police.html', context)


def dashboard(request):
    """
    View do painel de controle geral.
    Retorna informações sobre cargas, equipamentos e policiais.
    """
    data = {
        "loads": {
            "total": Load.objects.all().exclude(status="descarga").count(),
            "completed": Load.objects.filter(status="DESCARREGADA").count(),
            "pending": Load.objects.all().exclude(status="descarga").exclude(status="DESCARREGADA").count(),
        },
        "equipment": {
            "total": Equipment.objects.all().count(),
            "available": Equipment.objects.filter(status="disponível").count(),
            "unavailable": Equipment.objects.all().exclude(status="disponível").count(),
            "repair": Equipment.objects.all().filter(status="CONSERTO").count(),
            "judicial_request": Equipment.objects.all().filter(status="REQUISIÇÃO JUDICIAL").count(),
            "inactive": Equipment.objects.filter(Q(activated=False) | Q(activator=None)).count(),
            
        },
        "police": {
            "total": Police.objects.all().count(),
            "inactive": Police.objects.filter(Q(activated=False) | Q(activator=None)).count(),
            "fingerprints": Police.objects.all().exclude(fingerprint=None).count(),
        },
    }
    
    return render(request, 'dashboard.html', data)