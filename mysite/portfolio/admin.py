from django.contrib import admin
from .models import *


@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    pass

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    pass

@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    pass

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    filter_horizontal = ('tecnologias',)

@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    filter_horizontal = ('tecnologias',)