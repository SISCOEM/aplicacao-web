import datetime
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from SICOMB import settings
from django.utils import timezone
from police.models import Police

class Model_armament(models.Model):
    activator = models.ForeignKey(Police, on_delete=models.DO_NOTHING, default=None, null=True)
    activated = models.IntegerField("Ativado", default=0)
    model = models.TextField("Modelo do armamento")
    caliber = models.CharField("Calibre", choices=settings.AUX['calibres'], default="SELECIONE", max_length=30)
    description = models.TextField("Descrição")
    image_path = models.FileField(upload_to="Modelos/armamentos/")
    # amount

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"{self.model}"
    
    def get_amount(self):
        return Equipment.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id).count()


class Model_wearable(models.Model):
    activator = models.ForeignKey(Police, on_delete=models.DO_NOTHING, default=None, null=True)
    activated = models.IntegerField("Ativado", default=0)
    model = models.TextField("Modelo do vestimento")
    size = models.CharField("Tamanho", max_length=10)
    description = models.TextField("Descrição")
    image_path = models.FileField(upload_to="Modelos/vestiveis/")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"{self.model}"
    
    def get_amount(self):
        return Equipment.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id).count()
    

class Model_accessory(models.Model):  # bastão, escudo
    activator = models.ForeignKey(Police, on_delete=models.DO_NOTHING, default=None, null=True)
    activated = models.IntegerField("Ativado", default=0)
    model = models.TextField("Modelo do acessório")
    description = models.TextField("Descrição")
    image_path = models.FileField(upload_to="Modelos/acessorios/")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"{self.model}"
    
    def get_amount(self):
        return Equipment.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id).count()


class Model_grenada(models.Model):
    activator = models.ForeignKey(Police, on_delete=models.DO_NOTHING, default=None, null=True)
    activated = models.IntegerField("Ativado", default=0)
    model = models.TextField("Modelo da granada")
    image_path = models.FileField(upload_to="Modelos/granadas/")
    description = models.TextField("Descrição")
    
    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"{self.model}"

    def get_amount(self):
        return Equipment.objects.filter(model_type=ContentType.objects.get_for_model(self), model_id=self.id).count()


class Equipment(models.Model):
    CHOICES = (
        ("Disponível", "Disponível"),
        ("6H", "6H"),
        ("8H", "8H"),
        ("12H", "12H"),
        ("24H", "24H"),
        ("CONSERTO", "CONSERTO"),
        ("INDETERMINADO", "INDETERMINADO"),
        ("REQUISIÇÃO JUDICIAL", "REQUISIÇÃO JUDICIAL"),
    )
    date_register = models.DateTimeField("Data de registro", default=timezone.now)
    activator = models.ForeignKey(Police, on_delete=models.DO_NOTHING, default=None, null=True)
    activated = models.IntegerField("Ativado", default=0)
    serial_number = models.CharField("Numero de série", max_length=200, null=True, unique=True)
    uid = models.CharField("uid", max_length=200, primary_key=True, default=None)
    status = models.CharField("Estado atual", choices=CHOICES, max_length=20, default="Disponível")
    model_type = models.ForeignKey(ContentType, verbose_name="Tipo do modelo", on_delete=models.CASCADE)
    model_id = models.PositiveIntegerField(verbose_name="modelo")
    model = GenericForeignKey("model_type", "model_id")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"Equipamento {self.uid}"

    class Meta:
        verbose_name = "Equipamento"


class Bullet(models.Model):
    activator = models.ForeignKey(Police, on_delete=models.DO_NOTHING, default=None, null=True)
    activated = models.IntegerField("Ativado", default=0)
    amount = models.IntegerField("Quantidade", default=0)
    image_path = models.FileField(upload_to="Modelos/municoes/")
    caliber = models.CharField("Calibre", choices=settings.AUX['calibres'], default="SELECIONE", max_length=30, unique=True)
    description = models.TextField("Descrição")

    def __str__(self):
        # na hora dos campos do select ele retorna isso
        return f"{self.caliber}"
    
    def get_amount(self):
        return self.amount
