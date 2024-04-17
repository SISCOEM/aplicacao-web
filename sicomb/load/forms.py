from django import forms
from .models import Equipment_load, Load
from police.models import Police


class LoadForm(forms.ModelForm):
    date_load = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':''}), label='Data da Carga')
    
    class Meta:
        model = Load
        fields = '__all__'
        

class LoadFilterForm(forms.Form):
    turn_type = forms.CharField(
        label="Tipo de Turno",
        max_length=20,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control input-data'}, 
            choices=[
                ('', 'TODOS'), 
                ('6h', '6h'), 
                ('12h', '12h'), 
                ('24h', '24h'), 
                ('conserto', 'conserto'), 
                ('requisição judicial', 'requisição judicial'), 
                ('indeterminado', 'indeterminado'),
                ('descarga', 'descarga'),
            ]),
    )
    police = forms.ModelChoiceField(
        label="Policial",
        queryset=Police.objects.filter(tipo="Police"),  # Certifique-se de importar o modelo Police
        required=False,
        widget=forms.Select(attrs={'class': 'form-control input-data'}),
    )
    plate = forms.CharField(
        label="Matrícula", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'})
    )
    graduation = forms.CharField(
        label="Graduação", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'})
    )
    adjunct = forms.ModelChoiceField(
        label="Adjunto",
        queryset=Police.objects.filter(tipo="Adjunct"),  # Certifique-se de importar o modelo Police
        required=False,
        widget=forms.Select(attrs={'class': 'form-control input-data'}),
    )
    amount_items = forms.DecimalField(
        label="Quantidade de itens", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control input-data'}),
    )
    date_load_start = forms.DateTimeField(
        label="Data de Carregamento (início)", 
        required=False,
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local', 'class': 'form-control input-data'}),
    )
    date_load_end = forms.DateTimeField(
        label="Data de Carregamento (fim)", 
        required=False,
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local', 'class': 'form-control input-data'}),
    )
    expected_load_return_date_start = forms.DateTimeField(
        label="Data Prevista de Devolução (início)", 
        required=False,
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local', 'class': 'form-control input-data'}),
    )
    expected_load_return_date_end = forms.DateTimeField(
        label="Data Prevista de Devolução (fim)", 
        required=False,
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local', 'class': 'form-control input-data'}),
    )
    returned_load_date_start = forms.DateTimeField(
        label="Data de Descarregamento (início)", 
        required=False,
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local', 'class': 'form-control input-data'}),
    )
    returned_load_date_end = forms.DateTimeField(
        label="Data de Descarregamento (fim)", 
        required=False,
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local', 'class': 'form-control input-data'}),
    )
    equipment_sn = forms.CharField(
        label="Equipamento", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control input-data'})
    )
    status = forms.ChoiceField(
        label="Status",
        choices=(
            ('', "TODOS"), 
            ("ATRASADA", "ATRASADA"), 
            ("DATA DE RETORNO NÃO DEFINIDA", "DATA DE RETORNO NÃO DEFINIDA"), 
            ("DENTRO DO PRAZO", "DENTRO DO PRAZO"),
            ("DESCARREGADA", "DESCARREGADA"),
            ("DESCARREGADA COM ATRASO", "DESCARREGADA COM ATRASO"),
            ("PARCIALMENTE DESCARREGADA COM ATRASO", "PARCIALMENTE DESCARREGADA COM ATRASO"),
            ("PARCIALMENTE DESCARREGADA", "PARCIALMENTE DESCARREGADA"),
        ),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control input-data'}),
    )
    
    def filter_queryset(self, queryset):
        data = self.cleaned_data

        # Filtrar por tipo de turno
        turn_type = data.get('turn_type')
        if turn_type and turn_type != '':
            queryset = Load.objects.all()
            
            queryset = queryset.filter(turn_type=turn_type)

        # Filtrar por policial
        police = data.get('police')
        if police:
            queryset = queryset.filter(police=police)

        # Filtrar por placa
        plate = data.get('plate')
        if plate:
            queryset = queryset.filter(police__matricula__icontains=plate)

        # Filtrar por graduação
        graduation = data.get('graduation')
        if graduation:
            queryset = queryset.filter(police__posto__icontains=graduation)

        # Filtrar por adjunto
        adjunct = data.get('adjunct')
        if adjunct:
            queryset = queryset.filter(adjunct=adjunct)

        # Filtrar por quantidade de itens
        amount_items = data.get('amount_items')
        if amount_items:
            for i in queryset:
                equipment_loads = Equipment_load.objects.filter(load=i)
                
                if amount_items != len(equipment_loads):
                    queryset = queryset.exclude(pk=i.pk)
                    
        # Filtrar por datas
        date_load_start = data.get('date_load_start')
        date_load_end = data.get('date_load_end')
        expected_load_return_date_start = data.get('expected_load_return_date_start')
        expected_load_return_date_end = data.get('expected_load_return_date_end')
        returned_load_date_start = data.get('returned_load_date_start')
        returned_load_date_end = data.get('returned_load_date_end')

        if date_load_start:
            queryset = queryset.filter(date_load__gte=date_load_start)
        if date_load_end:
            queryset = queryset.filter(date_load__lte=date_load_end)
        if expected_load_return_date_start:
            queryset = queryset.filter(expected_load_return_date__gte=expected_load_return_date_start)
        if expected_load_return_date_end:
            queryset = queryset.filter(expected_load_return_date__lte=expected_load_return_date_end)
        if returned_load_date_start:
            queryset = queryset.filter(returned_load_date__gte=returned_load_date_start)
        if returned_load_date_end:
            queryset = queryset.filter(returned_load_date__lte=returned_load_date_end)

        # Filtrar por status
        status = data.get('status')
        if status and status != '':
            queryset = queryset.filter(status=status)
            
        equipment_sn = data.get('equipment_sn')
        if equipment_sn:
            list_loads = queryset
            queryset = []
            for load in list_loads:
                is_in = False
                for eq_load in Equipment_load.objects.filter(load=load):
                    if eq_load.equipment and eq_load.equipment.serial_number.lower() in equipment_sn.lower():
                        is_in = True
                        break
                    elif eq_load.bullet and eq_load.bullet.caliber.lower() in equipment_sn.lower():
                        is_in = True
                        break
                if is_in:
                    queryset.append(load)

        return queryset