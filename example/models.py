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


class Comunidade(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    anonima = models.BooleanField(default=False, verbose_name='Chat anônimo')
    administrador = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comunidades_admin')
    membros = models.ManyToManyField('User', blank=True, related_name='comunidades')
    membros_pendentes = models.ManyToManyField('User', blank=True, related_name='comunidades_pendentes')
    membros_silenciados = models.ManyToManyField('User', blank=True, related_name='comunidades_silenciadas')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comunidade'
        verbose_name_plural = 'Comunidades'
        ordering = ['-criado_em']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.administrador and not self.membros.filter(pk=self.administrador.pk).exists():
            self.membros.add(self.administrador)

    def approve_member(self, usuario):
        if not self.membros.filter(pk=usuario.pk).exists():
            self.membros.add(usuario)
        self.membros_pendentes.remove(usuario)

    def reject_member(self, usuario):
        self.membros_pendentes.remove(usuario)

    def request_membership(self, usuario):
        if not self.membros.filter(pk=usuario.pk).exists() and not self.membros_pendentes.filter(pk=usuario.pk).exists():
            self.membros_pendentes.add(usuario)

    def mute_member(self, usuario):
        if self.membros.filter(pk=usuario.pk).exists() and usuario != self.administrador:
            self.membros_silenciados.add(usuario)

    def unmute_member(self, usuario):
        self.membros_silenciados.remove(usuario)

    def is_muted(self, usuario):
        return self.membros_silenciados.filter(pk=usuario.pk).exists()

    def __str__(self):
        return self.nome


class Mensagem(models.Model):
    comunidade = models.ForeignKey('Comunidade', on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['criado_em']

    def __str__(self):
        autor_texto = self.autor.username if self.autor else 'Anônimo'
        return f'{autor_texto} @ {self.comunidade.nome}'


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