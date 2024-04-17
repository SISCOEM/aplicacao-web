from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from itertools import chain
from .templatetags.custom_filters import has_group
from django.contrib import messages
from django.db.models import Q

@has_group('admin')
def delete_equipment(request, id):
    """
    Descrição:
        Até o momento não foi necessário o uso
    """
    try:
        Equipment.objects.get(pk=id).delete()
    except Equipment.DoesNotExist:
        pass

    return redirect("filter_equipment")


@has_group('adjunct')
def test_tag(request):
    return render(request, "equipment/test_tag.html",)


@has_group('adjunct')
def register_edit_equipment(request, id=None):
    """
    Descrição da função:
    Pode registrar ou editar um equipamento a depender dos parametros recebidos

    Retorna:
        template: Em caso de sucesso redireciona para a tela de modelos, caso contrário retorna ao formulário
    """

    equipment = None
    if id:  # Se houver o id, signigica que é uma edição
        equipment = Equipment.objects.filter(pk=id, activated=True).exclude(activator=None).first()
        
        if not equipment:
            return render(
                request,
                "equipment/register-equipment.html",
                {"msm": "Equipamento não existe ou não está ativado!", "form": form},
            )

    if request.method == "POST":
        if request.POST.get("bullet") and request.POST.get("amount"):
            try:
                bullet = Bullet.objects.get(id=request.POST.get("bullet"))
            except Bullet.DoesNotExist:
                form = EquipmentForm()  # Se for bem sucedido ele zera o form

                return render(
                    request,
                    "equipment/register-equipment.html",
                    {"msm": "Munição não existe na base de dados!", "form": form},
                )
            bullet.amount = int(bullet.amount) + int(request.POST.get("amount"))
            bullet.save()
        else:
            form = EquipmentForm(request.POST, instance=equipment)
            if form.is_valid():
                form.save()

                return redirect("filter_equipment")
            else:
                return render(
                    request, "equipment/register-equipment.html", {"form": form}
                )
    settings.AUX["uids"] = []
    form = EquipmentForm(instance=equipment)  # Se for bem sucedido ele zera o form

    return render(request, "equipment/register-equipment.html", {"form": form})


@has_group('admin')
def register_edit_model(request, model_name=None, id=None):
    """
    Descrição da função:
    Pode registrar ou editar um modelo a depender dos parametros recebidos

    Parâmetros:
    model_name (str): Define o tipo do modelo a ser editado como bullet, accessory, wearable...
    id (int): Id do equipamento a ser editado.

    Retorna:
        template: Em caso de sucesso redireciona para a tela de modelos, caso contrário retorna ao formulário
    """

    model = None
    form = None

    if model_name:
        if model_name == "bullet":
            ModelClass = Bullet
            FormClass = BulletForm
        else:
            ModelClass = eval(f"Model_{model_name}")
            FormClass = eval(f"Model_{model_name}Form")

        if id:
            model = get_object_or_404(ModelClass, id=id)

        if request.method == "POST":
            form = FormClass(request.POST, request.FILES, instance=model)

            if form.is_valid():
                form.save()
                return redirect("manage_model")
        else:
            form = FormClass(instance=model)

    return render(
        request, "equipment/form-model.html", {"form": form, "model": model_name}
    )


@has_group('admin')
def delete_model(request, model_name=None, id=None):
    """
    Descrição:
        Até o momento não foi necessário o uso
    """
        
    data = {}
    if model_name:
        eval(f"Model_{model_name}.objects.get(pk=id).delete()")
        data["msm"] = "Deletado com sucesso!"

        return redirect("manage_model")
    else:
        print("Error delete_model")


@has_group('adjunct')
def filter_equipment(request):
    """
    Descrição:
        Retorna todos os equipamentos e filtra de acordo com o formulário preenchido
    """

    equipment_list = Equipment.objects.filter(activated=True).exclude(activator=None)
    filter_form = EquipmentFilterForm(request.GET)
    # filter_form = None
    if filter_form.is_valid():
        equipment_list = filter_form.filter_queryset(equipment_list)

    context = {
        'equipment_list': equipment_list,
        'filter_form': filter_form,
    }

    return render(request, 'equipment/filter-equipment.html', context)


@has_group('adjunct')
def filter_model(request):
    """
    Descrição:
        Retorna todos os modelos e filtra de acordo com o formulário preenchido
    """

    # Consulta todos os objetos dos diferentes modelos e os concatena
    all_models = list(chain(
        Model_armament.objects.filter(activated=True).exclude(activator=None),
        Model_accessory.objects.filter(activated=True).exclude(activator=None),
        Model_wearable.objects.filter(activated=True).exclude(activator=None),
        Model_grenada.objects.filter(activated=True).exclude(activator=None),
        Bullet.objects.filter(activated=True).exclude(activator=None)
    ))
    
    filter_form = ModelFilterForm(request.GET)
    
    if filter_form.is_valid():
        print("valido")
        all_models = filter_form.filter_queryset(all_models)
    
    context = {
        'model_list': all_models,
        'filter_form': filter_form,
    }

    return render(request, "equipment/filter-model.html", context)


@has_group('admin')
def approve_model(request):
    """
    Descrição:
        Função que aprova o modelo, e o torna ativado
    """

    if request.method == "POST":
        models = {
            "Acessório": Model_accessory,
            "Armamento": Model_armament,
            "Vestimentos": Model_wearable,
            "Granadas": Model_grenada,
            "Munição": Bullet,
        }
        
        model = models[request.POST.get("model_name")].objects.filter(pk=request.POST.get("model_id")).first()
        model.activator = request.user
        
        action = request.POST.get("action-type")
        if action:
            if action == 'approve':
                model.activated = 1
                model.save()
            elif action == 'disapprove':
                model.delete()
        
        else:
            messages.error(request, "Falha, ação indefinida!")
        
    all_models = list(chain(
        Model_armament.objects.filter(Q(activated=False) | Q(activator=None)),
        Model_accessory.objects.filter(Q(activated=False) | Q(activator=None)),
        Model_wearable.objects.filter(Q(activated=False) | Q(activator=None)),
        Model_grenada.objects.filter(Q(activated=False) | Q(activator=None)),
        Bullet.objects.filter(Q(activated=False) | Q(activator=None))
    ))
    
    context = {
        'model_list': all_models,
    }
    
    return render(request, "equipment/approve_model.html", context)


@has_group('admin')
def approve_equipment(request):
    """
    Descrição:
        Função que aprova o equipamento, e o torna ativado
    """
        
    equipment_list = Equipment.objects.filter(Q(activated=False) | Q(activator=None))

    if request.method == 'POST':
        equipment = Equipment.objects.filter(pk=request.POST.get("equipment_id")).first()
        equipment.activator = request.user
        
        action = request.POST.get("action-type")
        if action:
            if action == 'approve':
                equipment.activated = 1
                equipment.save()
            elif action == 'disapprove':
                equipment.delete()
        else:
            messages.error(request, "Falha, ação indefinida!")
    context = {
        'equipment_list': equipment_list,
    }
    return render(request, "equipment/approve_equipment.html", context)


@login_required
def get_equipment_info(request, pk):
    """
    Descrição da função:
        Retorna as informações de um equipamento
    """

    equipment = get_object_or_404(Equipment, pk=pk)
    
    equipment_info = equipment.serial_number #Teste, necessário modificações
    
    return render(request, "equipment/equipment_information.html", {'equipment': equipment, 'equipment_info': equipment_info})