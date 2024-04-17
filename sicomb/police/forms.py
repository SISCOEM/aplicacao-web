from django.contrib.auth.forms import UserCreationForm
from django import forms
from police.models import Police
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

from SICOMB import settings


class PoliceForm(forms.ModelForm):
    image_path = forms.ImageField(widget=forms.FileInput(attrs={'class':'file-input input-image', 'accept':'image/*', 'onchange':'handleFileSelection(event)'}), label='Foto')
    fingerprint = forms.CharField(widget=forms.HiddenInput(), label='Impressão Digital', required=False)
    class Meta:
        model = Police
        fields = [
            'username',
            'name',
            'matricula',
            'posto',
            'email',
            'telefone',
            'lotacao',
            'password',
            'image_path',
        ]
        
        widgets = {
            'username': forms.TextInput(attrs={'class':'input-data', "required": True}),
            'name': forms.TextInput(attrs={'class':'input-data', "required": True}),
            'matricula': forms.NumberInput(attrs={'id':'matricula-input'}),
            'posto': forms.Select(attrs={'class':'input-data select'}),
            'email': forms.EmailInput(attrs={'class':'input-data'}),
            'telefone': forms.TextInput(attrs={'class':'input-data'}),
            'lotacao': forms.TextInput(attrs={'class':'input-data'}),
            'password': forms.PasswordInput(attrs={'class':'input-data'}),
        }

    def clean_password(self):
        data = self.cleaned_data["password"]
        password = make_password(data)
        return password
    

class PoliceFilterForm(forms.Form):
    foto = forms.CharField(
        label="Foto",
        required=False,
        widget=forms.HiddenInput(),
    )
    name = forms.CharField(
        label="Nome",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'}),
    )
    email = forms.CharField(
        label="E-mail",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'}),
    )
    matricula = forms.DecimalField(
        label="Matrícula",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control input-data'}),
    )
    telefone = forms.CharField(
        label="Telefone",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'}),
    )
    lotacao = forms.CharField(
        label="Lotação",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'}),
    )
    posto = forms.ChoiceField(
        label="Posto",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control input-data'}),
    )
    tipo = forms.ChoiceField(
        label="Tipo",
        choices=[(None, "-------------"), ("Policial", "Policial"), ("Adjunto", "Adjunto"), ("Administrador", "Administrador")],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control input-data'}),
    )
    activator = forms.CharField(
        label="Policial Aprovador",
        required=False,
        widget=forms.HiddenInput(),
    )

    def filter_queryset(self, queryset):
        data = self.cleaned_data

        if data.get('email'):
            queryset = queryset.filter(email__icontains=data['email'])
        if data.get('name'):
            queryset = queryset.filter(name__icontains=data['name'])
        if data.get('matricula'):
            queryset = queryset.filter(matricula__icontains=data['matricula'])
        if data.get('telefone'):
            queryset = queryset.filter(telefone__icontains=data['telefone'])
        if data.get('lotacao'):
            queryset = queryset.filter(lotacao__icontains=data['lotacao'])
        if data.get('posto'):
            queryset = queryset.filter(posto__icontains=data['posto'])
        if data.get('tipo'):
            queryset = queryset.filter(tipo=data['tipo'])
        # if data.get('activator') is not None:
        #     queryset = queryset.filter(activator=data['activator'])

        return queryset


