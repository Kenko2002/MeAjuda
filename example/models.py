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

class Convenio(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Instituicao(models.Model):

    TIPO_PESSOA_CHOICES = [
        ("PJ", "Pessoa Jurídica"),
        ("PF", "Pessoa Física"),
    ]

    nome = models.CharField(max_length=255)
    tipo_pessoa = models.CharField(max_length=2, choices=TIPO_PESSOA_CHOICES)

    cpf = models.CharField(max_length=14, blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True)

    area_atuacao = models.CharField(max_length=255)

    responsavel = models.CharField(
        max_length=255,
        verbose_name="Responsável (CEO)"
    )

    # Endereço
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    # Localização
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Contatos
    telefone_principal = models.CharField(max_length=20)
    telefone_secundario = models.CharField(
        max_length=20,
        blank=True
    )

    whatsapp = models.CharField(max_length=20, blank=True)
    telegram = models.CharField(max_length=100, blank=True)

    email = models.EmailField()

    website = models.URLField(blank=True)

    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    # Atendimento
    horario_atendimento = models.TextField(
        help_text="Ex: Seg-Sex 08:00 às 18:00"
    )

    # Relacionamentos
    convenios = models.ManyToManyField(
        Convenio,
        blank=True
    )

    tags = models.ManyToManyField(
        "TagProblema",
        blank=True
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

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