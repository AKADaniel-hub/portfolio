from django.contrib import admin
from .models import Artigo, Comentario


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao', 'total_likes')
    search_fields = ('titulo', 'autor__username')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'autor', 'data_criacao')