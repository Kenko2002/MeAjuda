from django.contrib.auth.models import AbstractUser
from django.db import models

class TagProblema(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    problemas = models.ManyToManyField(TagProblema, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class Instituicao(models.Model):
    nome = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tags = models.ManyToManyField(TagProblema)

    def __str__(self):
        return self.nome

class RecursoAjuda(models.Model):
    TIPO_CHOICES = [('TEL', 'Telefone'), ('SITE', 'Site'), ('RED', 'Rede Social')]
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)
    valor = models.CharField(max_length=255)
    tag = models.ForeignKey(TagProblema, on_delete=models.CASCADE)
    TIPO_CHOICES = [
        ('TEL', 'Telefone'),
        ('SITE', 'Site'),
        ('RED', 'Rede Social'),
    ]
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)
    valor = models.CharField(max_length=255)  # URL ou Número
    tag = models.ForeignKey(TagProblema, on_delete=models.CASCADE, related_name='recursos')

    def __str__(self):
        return f"{self.titulo} ({self.tag.nome})"