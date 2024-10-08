from itertools import chain
from django import forms
from equipment.models import *
from django.utils.translation import gettext_lazy as _


class EquipmentForm(forms.ModelForm):
    OPCOES = [
        ("", "SELECIONE"),
        ("wearable", "VESTÍVEL"),
        ("accessory", "ACESSÓRIO"),
        ("armament", "ARMAMENTO"),
        ("grenada", "GRANADA"),
    ]

    uid = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"id": "input-uid", "style": "display: none"}),
        label="",
    )
    serial_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-data", "id": "serial-number-input", "placeholder": "Número de série"}),
        label="Número de Série",
    )
    type = forms.CharField(
        widget=forms.Select(attrs={"class": "select-field", "id": "type-choices"}, choices=OPCOES),
        label="Tipo",
    )
    
    armament = forms.ModelChoiceField(
        queryset=Model_armament.objects.filter(activated=True).exclude(activator=None),
        widget=forms.Select(attrs={"id": "type-choices-armament", "style": "display: none", "class": "type-choices-type select-field", "name": "model"}),
        label="ARMAMENTOS",
        empty_label="SELECIONE",
        required=False,
    )
    accessory = forms.ModelChoiceField(
        queryset=Model_accessory.objects.filter(activated=True).exclude(activator=None),
        widget=forms.Select(attrs={"id": "type-choices-accessory", "style": "display: none", "class": "type-choices-type select-field", "name": "model"}),
        label="ACESSÓRIOS",
        empty_label="SELECIONE",
        required=False,
    )
    wearable = forms.ModelChoiceField(
        queryset=Model_wearable.objects.filter(activated=True).exclude(activator=None),
        widget=forms.Select(attrs={"id": "type-choices-wearable", "style": "display: none", "class": "type-choices-type select-field", "name": "model"}),
        label="VESTIMENTOS",
        empty_label="SELECIONE",
        required=False,
    )
    grenada = forms.ModelChoiceField(
        queryset=Model_grenada.objects.filter(activated=True).exclude(activator=None),
        widget=forms.Select(attrs={"id": "type-choices-grenada", "style": "display: none", "class": "type-choices-type select-field", "name": "model"}),
        label="GRANADAS",
        empty_label="SELECIONE",
        required=False,
    )
    
    def save(self, commit=True):
        equipment = super().save(commit=False)
        
        # Define o tipo de modelo com base na escolha feita no campo "type"
        if self.cleaned_data['type'] == 'armament':
            equipment.model = self.cleaned_data['armament']
        elif self.cleaned_data['type'] == 'accessory':
            equipment.model = self.cleaned_data['accessory']
        elif self.cleaned_data['type'] == 'wearable':
            equipment.model = self.cleaned_data['wearable']
        elif self.cleaned_data['type'] == 'grenada':
            equipment.model = self.cleaned_data['grenada']

        if commit:
            equipment.save()
        return equipment

    class Meta:
        model = Equipment
        fields = ["uid", "serial_number", "type", "status"]
        
        widgets = {
            "status" : forms.Select(attrs={"class": "select-field"}),
        }


class Model_grenadaForm(forms.ModelForm):
    
    class Meta:
        model = Model_grenada
        fields = [
            "model",
            "image_path",
            "description",
        ] 
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "model": forms.TextInput(attrs={"class": "input-data", "placeholder": "Modelo"}),
            "image_path": forms.FileInput(attrs={"class": "input-file input-image", "id":"file", "accept":"image/*"})
        }
        
        
class Model_armamentForm(forms.ModelForm):
    
    class Meta:
        model = Model_armament
        fields = [
            "caliber",
            "model",
            "image_path",
            "description",
        ] 
        # Tava bugando ent coloquei aqui
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "caliber": forms.Select(attrs={"class": "select-field", "placeholder": "Calibre"}),
            "model": forms.TextInput(attrs={"class": "input-data", "placeholder": "Modelo"}),
            "image_path": forms.FileInput(attrs={"class": "input-file input-image", "id":"file", "accept":"image/*"})
        }
        
class Model_wearableForm(forms.ModelForm):
    
    class Meta:
        model = Model_wearable
        fields = [
            "size",
            "model",
            "image_path",
            "description",
        ] 
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "size": forms.TextInput(attrs={"class": "input-data", "placeholder": "Tamanho"}),
            "model": forms.TextInput(attrs={"class": "input-data", "placeholder": "Modelo"}),
            "image_path": forms.FileInput(attrs={"class": "input-file input-image", "id":"file", "accept":"image/*"})
        }
        
class Model_accessoryForm(forms.ModelForm):
    
    class Meta:
        model = Model_accessory
        fields = [
            "model",
            "image_path",
            "description",
        ] 
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "model": forms.TextInput(attrs={"class": "input-data", "placeholder": "Modelo"}),
            "image_path": forms.FileInput(attrs={"class": "input-file input-image", "id":"file", "accept":"image/*"})
        }
        

class BulletForm(forms.ModelForm):
    
    class Meta:
        model = Bullet
        fields = [
            "amount",
            "caliber",
            "image_path",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "caliber": forms.Select(attrs={"class": "select-field", "placeholder": "Calibre"}),
            "amount": forms.NumberInput(attrs={"class": "input-data", "placeholder": "Modelo", "min":0}),
            "image_path": forms.FileInput(attrs={"class": "input-file input-image", "id":"file", "accept":"image/*"})
        }
        

class EquipmentFilterForm(forms.Form):
    equipment_choices = Equipment.CHOICES
    equipment_choices += ((None, "-----------"),)
    
    models_eqipment = (
        (None, '----------'),
        (ContentType.objects.get(app_label='equipment', model='model_armament').pk, 'Armamento'),
        (ContentType.objects.get(app_label='equipment', model='model_accessory').pk, 'Acessório'),
        (ContentType.objects.get(app_label='equipment', model='model_wearable').pk, 'Vestimentos'),
        (ContentType.objects.get(app_label='equipment', model='model_grenada').pk, 'Granadas'),
    )

    serial_number = forms.CharField(
        label=_("Número de Série"), 
        max_length=200, required=False, 
        widget=forms.TextInput(
            attrs={'class': 'form-control input-data'}),
    )
    status = forms.ChoiceField(
        label=_("Estado Atual"),
        choices=equipment_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control input-data'}),
    )
    model_type = forms.ChoiceField(
        label=_("Tipo do Modelo"),
        choices=models_eqipment,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control input-data'}),
    )
    
    model = forms.CharField(
        label=_("Modelo"), 
        max_length=200, 
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control input-data'}),
    )
    
    activator = forms.CharField(
        label="Policial Aprovador",
        required=False,
        widget=forms.HiddenInput(),
    )

    def filter_queryset(self, queryset):
        data = self.cleaned_data

        if data.get('serial_number'):
            queryset = queryset.filter(serial_number__icontains=data['serial_number'])
        if data.get('status'):
            queryset = queryset.filter(status__icontains=data['status'])
        if data.get('model_type'):
            queryset = queryset.filter(model_type=data['model_type'])
        # if data.get('activator'):
        #     queryset = queryset.filter(activator=data['activator'])
        if data.get('model'):
            queryset = [i for i in queryset.all() if data['model'].lower() in i.model.model.lower()]

        return queryset


class ModelFilterForm(forms.Form):
    TYPES = (
        ('Model_armament', 'Armamento'),
        ('Model_accessory', 'Acessório'),
        ('Model_wearable', 'Vestimentos'),
        ('Model_grenada', 'Granadas'),
        ('Bullet', 'Munição'),
    )
    
    type = forms.MultipleChoiceField(
        label=_("Tipo do Modelo"), 
        choices=TYPES, 
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control checkboxes '}),
    )
    
    amount = forms.DecimalField(
        label=_("Quantidade"),
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control input-data'}),
    )
    
    caliber = forms.MultipleChoiceField(
        label=_("Calibre"), 
        choices=settings.AUX['calibres'],
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control input-data select-multiple'}),
    )
    
    model = forms.CharField(
        label=_("Modelo"), 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'}),
    )
    
    description = forms.CharField(
        label=_("Descrição"), 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'}),
    )
    
    size = forms.CharField(
        label=_("Tamanho"), 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'}),
    )
    
    activator = forms.CharField(
        label="Policial Aprovador",
        required=False,
        widget=forms.HiddenInput(),
    )
    
    def filter_queryset(self, queryset):
        data = self.cleaned_data
        
        if data.get("type"):
            queryset = []
            
            model_classes = {
                'Model_armament': Model_armament,
                'Model_accessory': Model_accessory,
                'Model_wearable': Model_wearable,
                'Model_grenada': Model_grenada,
                'Bullet': Bullet,
            }
            for i in data.get("type"):
                if not i == 'Bullet':
                    models_aux = model_classes[i].objects.filter(activated=True).exclude(activator=None)
                    queryset = list(chain(queryset, models_aux))
                else:
                    models_aux = model_classes[i].objects.all()
                    queryset = list(chain(queryset, models_aux))
                    
        
        print(data["amount"])
        if data["amount"]:
            queryset = [obj for obj in queryset if hasattr(obj, 'amount') and obj.amount == data.get("amount")]

        if data.get("caliber") and data.get("caliber")[0] != '':
            print(data.get("caliber"))
            queryset = [obj for obj in queryset if hasattr(obj, "caliber") and obj.caliber in data.get("caliber")]

        if data.get("model"):
            queryset = [obj for obj in queryset if hasattr(obj, "model") and data.get("model").lower() in obj.model.lower()]

        if data.get("description"):
            queryset = [obj for obj in queryset if hasattr(obj, "description") and data.get("description").lower() in obj.description.lower()]

        if data.get("size"):
            queryset = [obj for obj in queryset if hasattr(obj, 'size') and data.get("size").lower() in obj.size.lower()]
            
        return queryset