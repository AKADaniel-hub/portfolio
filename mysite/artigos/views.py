from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from .models import Artigo, Comentario
from .forms import ArtigoForm, ComentarioForm, RegistoAutorForm


def e_autor(user):
    return user.is_authenticated and user.groups.filter(name='autores').exists()


def artigos_view(request):
    artigos = Artigo.objects.select_related('autor').all()
    return render(request, 'artigos/artigos.html', {'artigos': artigos})


def artigo_view(request, id):
    artigo = get_object_or_404(Artigo.objects.select_related('autor').prefetch_related('comentarios__autor'), id=id)
    comentario_form = ComentarioForm()

    if request.method == 'POST' and request.user.is_authenticated:
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            c = comentario_form.save(commit=False)
            c.artigo = artigo
            c.autor = request.user
            c.save()
            return redirect('artigos:artigo', id=artigo.id)

    return render(request, 'artigos/artigo.html', {
        'artigo': artigo,
        'comentario_form': comentario_form,
    })


@login_required
def artigo_like_view(request, id):
    artigo = get_object_or_404(Artigo, id=id)
    if request.user in artigo.likes.all():
        artigo.likes.remove(request.user)
    else:
        artigo.likes.add(request.user)
    return redirect('artigos:artigo', id=artigo.id)


@login_required
def artigo_criar_view(request):
    if not e_autor(request.user):
        raise PermissionDenied
    form = ArtigoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        return redirect('artigos:artigos')
    return render(request, 'artigos/artigo_form.html', {'form': form, 'titulo': 'Novo Artigo'})


@login_required
def artigo_editar_view(request, id):
    artigo = get_object_or_404(Artigo, id=id)
    if not e_autor(request.user) or artigo.autor != request.user:
        raise PermissionDenied
    form = ArtigoForm(request.POST or None, request.FILES or None, instance=artigo)
    if form.is_valid():
        form.save()
        return redirect('artigos:artigo', id=artigo.id)
    return render(request, 'artigos/artigo_form.html', {'form': form, 'titulo': 'Editar Artigo'})


@login_required
def artigo_apagar_view(request, id):
    artigo = get_object_or_404(Artigo, id=id)
    if not e_autor(request.user) or artigo.autor != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        artigo.delete()
        return redirect('artigos:artigos')
    return render(request, 'artigos/artigo_confirmar_apagar.html', {'artigo': artigo})


def registo_autor_view(request):
    if request.user.is_authenticated:
        return redirect('artigos:artigos')
    if request.method == 'POST':
        form = RegistoAutorForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo, _ = Group.objects.get_or_create(name='autores')
            user.groups.add(grupo)
            login(request, user)
            return redirect('artigos:artigos')
    else:
        form = RegistoAutorForm()
    return render(request, 'artigos/registo.html', {'form': form})