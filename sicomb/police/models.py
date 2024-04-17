from django.db import models
from django.contrib.auth.models import AbstractUser
from SICOMB import settings
from django.contrib.auth.models import Group


class Police(AbstractUser):
    name = models.CharField("Nome", max_length=200, unique=True)
    activator = models.ForeignKey('self', on_delete=models.DO_NOTHING, default=None, null=True)
    activated = models.IntegerField("Ativado", default=0)
    matricula = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20, unique=True)
    lotacao = models.CharField(max_length=50)
    posto = models.CharField("Posto/Graduação", max_length=50, choices=settings.AUX['postos'])
    image_path = models.FileField(upload_to="policiais/%Y-%m-%d/")
    tipo = models.CharField(max_length=20, default="Policial", choices=[("Policial", "Policial"), ("Adjunto","Adjunto"), ("Administrador", "Administrador")])
    fingerprint = models.CharField(max_length=250, null=True, default=None)

    class Meta:
        verbose_name = 'Policial'
        verbose_name_plural = 'Policiais'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        created = not self.pk  # Verifica se o objeto está sendo criado (não tem chave primária)
        super(Police, self).save(*args, **kwargs)  # Chama o método save da classe pai

        if created:
            group_police, _ = Group.objects.get_or_create(name='police')
            self.groups.add(group_police)
        
        