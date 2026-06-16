from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TagProblema, Instituicao, RecursoAjuda, Convenio, Comunidade, Mensagem 

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações de Ajuda', {'fields': ('bio', 'problemas')}),
    )
    filter_horizontal = ('problemas',)

@admin.register(TagProblema)
class TagProblemaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_pessoa', 'area_atuacao', 'cidade', 'estado')
    list_filter = ('tipo_pessoa', 'area_atuacao', 'estado')

@admin.register(RecursoAjuda)
class RecursoAjudaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'tag')
    list_filter = ('tipo', 'tag')
    
@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Comunidade)
class ComunidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'administrador', 'anonima', 'criado_em')
    list_filter = ('anonima',)
    search_fields = ('nome', 'descricao', 'administrador__username')
    filter_horizontal = ('membros', 'membros_pendentes', 'membros_silenciados')

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('comunidade', 'autor', 'criado_em')
    list_filter = ('comunidade',)
    search_fields = ('texto', 'autor__username')