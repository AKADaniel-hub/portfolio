from django.contrib import admin
from .models import *


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'grau')
    search_fields = ('nome', 'sigla')


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome', 'email')


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'em_uso')
    search_fields = ('nome',)
    list_filter = ('tipo', 'em_uso')


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'unidade_curricular', 'classificacao', 'destaque')
    search_fields = ('titulo', 'descricao', 'conceitos_aplicados')
    list_filter = ('destaque', 'unidade_curricular')
    filter_horizontal = ('tecnologias',)
    fields = (
        'titulo', 'descricao', 'conceitos_aplicados',
        'tecnologias', 'unidade_curricular',
        'repositorio_github', 'video_demo',
        'data_realizacao', 'classificacao', 'destaque', 'imagem',
    )


@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'orientador', 'licenciatura', 'classificacao', 'destaque')
    search_fields = ('titulo', 'autor', 'orientador')
    list_filter = ('destaque', 'licenciatura')
    filter_horizontal = ('tecnologias',)
    fields = (
        'titulo', 'autor', 'orientador', 'licenciatura',
        'resumo', 'areas', 'palavras_chave',
        'tecnologias', 'pdf', 'imagem',
        'classificacao', 'destaque', 'url_repositorio',
    )