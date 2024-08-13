import json
from django import template
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from equipment.models import Equipment
from police.models import Police
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Q

register = template.Library()

@register.filter
def model_class(model):
    model_name = {
        'Model_armament': 'Armamento',
        'Model_accessory': 'Acessório',
        'Model_wearable': 'Vestimentos',
        'Model_grenada': 'Granadas',
        'Bullet': 'Munição',
    }
    
    return model_name[model.__class__.__name__]


@register.filter
def get_amount(model):
    try:
        if model is not None:
            return model.get_amount()
    except Exception as e:
        print(f"Erro ao acessar 'model': {e}")

    return '-'
    

@register.filter(name='replace_underscore')
def replace_underscore(value):
    return value.replace('_', ' ')

def require_user_pass(funcao):
    """
    Faz a validação das credenciais passadas a cada requisição
    """

    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            json_data = request.POST
            
            password = json_data.get('pass')
            user = json_data.get('user')
            police = Police.objects.filter(Q(name=user) | Q(username=user), password=password).first()
            
            if police:
                if police.groups.filter(name="adjunct").exists() or police.is_superuser:
                    return funcao(request, *args, **kwargs)
                else:
                    return JsonResponse({"msm": "Usuário não tem permissão!"}, status=403, json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({"msm": "Credenciais inválidas"}, status=401, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"msm": "Método não suportado"}, status=405, json_dumps_params={'ensure_ascii': False})
        
    return wrapper


def has_group(group_name):
    """
    Descrição:
        verifica se o usuário logado tem determinada permissão
    """
    
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Verifica se o usuário está autenticado
            if not request.user.is_authenticated:
                print("Acesso negado. Você não está autenticado.")
                messages.error(request, "Acesso negado. Você não está autenticado.")
                return render(request, "error.html")
            
            if isinstance(group_name, list):
                # Verifica se o usuário pertence ao grupo especificado
                for i in group_name:
                    if request.user.groups.filter(name=i).exists() or request.user.is_superuser:
                        return view_func(request, *args, **kwargs)
                print("Acesso negado. Você não tem permissão para acessar esta página.")
                messages.error(request, "Acesso negado. Você não tem permissão para acessar esta página.")
                return render(request, "error.html")
            
            else:
                if request.user.groups.filter(name=group_name).exists() or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                print("Acesso negado. Você não tem permissão para acessar esta página.")
                messages.error(request, "Acesso negado. Você não tem permissão para acessar esta página.")
                return render(request, "error.html")
        
        return wrapper
    
    return decorator
