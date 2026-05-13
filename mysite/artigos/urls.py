from django.urls import path
from . import views

app_name = 'artigos'

urlpatterns = [
    path('', views.artigos_view, name='artigos'),
    path('<int:id>/', views.artigo_view, name='artigo'),
    path('<int:id>/like/', views.artigo_like_view, name='like'),
    path('novo/', views.artigo_criar_view, name='artigo_criar'),
    path('<int:id>/editar/', views.artigo_editar_view, name='artigo_editar'),
    path('<int:id>/apagar/', views.artigo_apagar_view, name='artigo_apagar'),
    path('registo/', views.registo_autor_view, name='registo'),
]