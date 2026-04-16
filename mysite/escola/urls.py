from django.urls import path
from . import views

app_name = 'escola'

urlpatterns = [
    path('cursos/', views.cursos_view, name='cursos'),
    path('', views.cursos_view),   #  rota que abre diretamente a página dos cursos
    path('cursos/<int:id>/', views.curso_view, name='curso'),
    path('professores/', views.professores_view, name='professores'),
    path('alunos/', views.alunos_view, name='alunos'),
]