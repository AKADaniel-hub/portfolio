from django.urls import path
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('makingof/', views.makingof_view, name='makingof'),

    path('projetos/', views.projetos_view, name='projetos'),
    path('projetos/novo/', views.projeto_criar_view, name='projeto_criar'),
    path('projetos/<int:id>/editar/', views.projeto_editar_view, name='projeto_editar'),
    path('projetos/<int:id>/apagar/', views.projeto_apagar_view, name='projeto_apagar'),

    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('tecnologias/nova/', views.tecnologia_criar_view, name='tecnologia_criar'),
    path('tecnologias/<int:id>/editar/', views.tecnologia_editar_view, name='tecnologia_editar'),
    path('tecnologias/<int:id>/apagar/', views.tecnologia_apagar_view, name='tecnologia_apagar'),

    path('ucs/', views.ucs_view, name='ucs'),

    path('competencias/', views.competencias_view, name='competencias'),
    path('competencias/nova/', views.competencia_criar_view, name='competencia_criar'),
    path('competencias/<int:id>/editar/', views.competencia_editar_view, name='competencia_editar'),
    path('competencias/<int:id>/apagar/', views.competencia_apagar_view, name='competencia_apagar'),

    path('formacoes/', views.formacoes_view, name='formacoes'),
    path('formacoes/nova/', views.formacao_criar_view, name='formacao_criar'),
    path('formacoes/<int:id>/editar/', views.formacao_editar_view, name='formacao_editar'),
    path('formacoes/<int:id>/apagar/', views.formacao_apagar_view, name='formacao_apagar'),

    path('tfcs/', views.tfcs_view, name='tfcs'),
]