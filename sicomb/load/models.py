from datetime import datetime
import threading
from django.db import models
from equipment.models import Equipment, Bullet
from police.models import Police
from django.utils import timezone
from django.db.models import Q
from django.core.mail import EmailMessage
import pdfkit
from django.template.loader import render_to_string
from report.models import *
from django.db import transaction


class LoadManager(models.Manager):
    def get_load_pdf(self, load, pdf_path=False):
        """
        Gera relatório de carga em pdf
        """
        context = {
            "load": load,
            "equipment_loads": self.get_equipment_loads(load)
        }
        
        options = {
            'page-size': 'A4',
            'encoding': 'UTF-8'
        }
        
        html = render_to_string('load/pdf_template.html', context)
        return pdfkit.from_string(html, pdf_path, options=options)
    

    def check_all_loads(self):
        """
        Checa o status de cada carga em aberto,e define seu status como atrasada, parcialmente devolvida com atraso...
        """

        def chek():
            for i in Load.objects.exclude(status="DESCARREGADA").exclude(turn_type="descarga"):
                Load.objects.check_load(i)
                
        thread = threading.Thread(target=chek)
        thread.start()
        
        
    def check_load(self, load):
        """
        Faz o check, compara as datas e atualiza os status
        """
        
        data_hora_atual = timezone.now()
        expected_return_date = load.expected_load_return_date
        
        # se tem alguma que já foi devolvida
        has_devolved = load.equipment_loads.filter(Q(status='Devolvido') | Q(status="Justificado")).exists()
        # se tem alguma que ainda não foi devolvida
        has_not_devolved = load.equipment_loads.exclude(Q(status='Devolvido') | Q(status='Justificado')).exists()
        
        status_descarregado = ['DESCARREGADA', 'DESCARREGADA COM ATRASO']
        
        if load.turn_type != 'descarga':
            if load.status not in status_descarregado: 
                if expected_return_date:
                    if data_hora_atual > expected_return_date:
                        if has_devolved:
                            if has_not_devolved:
                                load.status = 'PARCIALMENTE DESCARREGADA COM ATRASO'
                            else:
                                load.status = 'DESCARREGADA COM ATRASO'
                            load.returned_load_date = datetime.now()
                        else:
                            load.status = 'ATRASADA'
                    else:
                        if has_devolved:
                            if has_not_devolved:
                                load.status = 'PARCIALMENTE DESCARREGADA'
                            else:
                                load.status = 'DESCARREGADA'
                            load.returned_load_date = datetime.now()
                        else:
                            load.status = 'DENTRO DO PRAZO'
                else:
                    if has_devolved:
                        if has_not_devolved:
                            load.status = 'PARCIALMENTE DESCARREGADA'
                        else:
                            load.status = 'DESCARREGADA'
                            if load.returned_load_date is None:
                                load.returned_load_date = data_hora_atual
                                load.save()
                    else:
                        load.status = 'DATA DE RETORNO NÃO DEFINIDA'
            elif load.returned_load_date is None: # Forma provisória de resolver erro de cargas como CONSERTO e REQUISIÇÃO sem data
                load.returned_load_date = data_hora_atual
                load.save()
        else:
            load.status = 'descarga'
                    
        load.save()
        return True
    
    
    def generate_load_report(self, load, subject):
        """
        Adiciona ao banco de relatórios gerados, (pode ser invalidado no backup para poupar espaço)
        """

        with transaction.atomic():
            report = Report.objects.create(title=subject)

            load_info = [
                ["Data de Carga:", load.date_load.strftime('%d/%m/%Y %H:%M')],
                ["Data Prevista de Devolução:", load.expected_load_return_date.strftime('%d/%m/%Y %H:%M') if load.expected_load_return_date else 'N/A'],
                ["Data de Descarregamento:", load.returned_load_date.strftime('%d/%m/%Y %H:%M') if load.returned_load_date else 'N/A'],
                ["Tipo de Turno:", load.turn_type],
                ["Status:", load.status],
                ["Policial:", load.police.name],
                ["Adjunto:", load.adjunct.name],
            ]

            for field, content in load_info:
                Report_field.objects.create(report=report, field=field, content=content)

            Report_field.objects.create(report=report, field="Informações dos equipamentos", content=None)

            for equipment_load in load.equipment_loads.all():
                Report_field.objects.create(
                    report=report,
                    field="Equipamento",
                    content=equipment_load.equipment.model.model if equipment_load.equipment else equipment_load.bullet,
                )
                Report_field.objects.create(report=report, field="Quantidade", content=str(equipment_load.amount))
                Report_field.objects.create(report=report, field="Observação", content=equipment_load.observation if equipment_load.observation else 'N/A')
                Report_field.objects.create(report=report, field="Status", content=equipment_load.status)

        return report
    

    def send_relatory(self, load, to=False):
        """
        Manda o relatório como um email para o destinatário definido, caso não seja definido um destinatário ele manda para o policial da carga
        """
        def send():
            pdf = self.get_load_pdf(load)
            
            subject = 'Relatório de carga'
            message = f'Relatório da carga feita no dia {load.date_load}' if load.turn_type != "descarga" else f'Relatório da descarga feita no dia {load.date_load}'
            from_email = load.adjunct.email
            
            self.generate_load_report(load, subject)
            
            if not to:
                recipient_list = [load.police.email]
            else:
                recipient_list = [to]
            
            email = EmailMessage(
                subject=subject,
                body=message,
                bcc=recipient_list,
            )
            
            email.attach(f'Relatório da carga {load.id}.pdf', pdf, 'application/pdf')
            email.send()
            
        thread = threading.Thread(target=send)
        thread.start()

        # Retorna a referência à thread (opcional, dependendo dos requisitos)
        return thread
    

    def get_equipment_loads(self, load):
        return Equipment_load.objects.filter(load=load)


class Load(models.Model):
    load_unload = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date_load = models.DateTimeField(default=timezone.now)
    expected_load_return_date = models.DateTimeField(
        "Data Prevista de Devolução", null=True
    )
    returned_load_date = models.DateTimeField("Data de Descarregamento", null=True)
    turn_type = models.CharField(max_length=20)
    status = models.CharField(
        "horário_carga",
        max_length=50,
        default="DENTRO DO PRAZO",
        choices=(
            ("Devolvido", "Devolvido"), 
            ("Pendente", "Pendente"), 
            ("Parcialmente devolvido", "Parcialmente devolvido"),
            ("Justificado", "Justificado"),
        ),
    )
    police = models.ForeignKey(
        Police, on_delete=models.DO_NOTHING, related_name="policial"
    )
    adjunct = models.ForeignKey(
        Police, on_delete=models.DO_NOTHING, related_name="adjunto"
    )
    
    objects = LoadManager()

    def __str__(self):
        return str(self.pk)


# Tabela que faz o relacionamento entre a carga e os equipamentos
class Equipment_load(models.Model):
    """
    Classe associatica em que vinculamos os equipamento à carga, formando uma relação de 1 carga pra muitas Equipment_load's. Caso o equipamento seja uma munição, o campo de equipment fica vazia e o campo de munição é preenchido.

    Cada Equipment_load tem seu status afinal pode acontecer de somente uma parte da carga ser devolvida.
    """

    load = models.ForeignKey(Load, on_delete=models.CASCADE, related_name='equipment_loads')
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, null=True, default=None
    )
    bullet = models.ForeignKey(
        Bullet, on_delete=models.CASCADE, null=True, default=None
    )
    # o amount diz, caso seja uma munição, a quantidade selecionada nessa carga em específico e dessa munição em específico
    amount = models.IntegerField("Quantidade", null=True, default="1")
    observation = models.TextField("Observação", default=None, null=True)
    status = models.CharField(
        "Status",
        max_length=20,
        default="Pendente",
        choices=(
            ("Devolvido", "Devolvido"), 
            ("Pendente", "Pendente"),
            ("Justificado", "Justificado"),
        ),
    )



