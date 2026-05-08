from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Projeto, Tecnologia, UnidadeCurricular, Competencia, Formacao, TFC
from .forms import ProjetoForm, TecnologiaForm, UnidadeCurricularForm, CompetenciaForm, FormacaoForm


def e_gestor(user):
    return user.is_authenticated and user.groups.filter(name='gestor-portfolio').exists()

def index_view(request):
    return render(request, 'portfolio/index.html')

def sobre_view(request):
    return render(request, 'portfolio/sobre.html')

def makingof_view(request):
    return render(request, 'portfolio/makingof.html')

# Projetos
def projetos_view(request):
    projetos = Projeto.objects.prefetch_related('tecnologias').all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})

@login_required
def projeto_criar_view(request):
    if not e_gestor(request.user): raise PermissionDenied
    form = ProjetoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/novo_projeto.html', {'form': form})

@login_required
def projeto_editar_view(request, id):
    if not e_gestor(request.user): raise PermissionDenied
    projeto = get_object_or_404(Projeto, id=id)
    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/edita_projeto.html', {'form': form, 'projeto': projeto})

@login_required
def projeto_apagar_view(request, id):
    if not e_gestor(request.user): raise PermissionDenied
    projeto = get_object_or_404(Projeto, id=id)
    if request.method == 'POST':
        projeto.delete()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/projetos.html', {'projetos': Projeto.objects.all()})

# Tecnologias
def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})

@login_required
def tecnologia_criar_view(request):
    if not e_gestor(request.user): raise PermissionDenied
    form = TecnologiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/nova_tecnologia.html', {'form': form})

@login_required
def tecnologia_editar_view(request, id):
    if not e_gestor(request.user): raise PermissionDenied
    tecnologia = get_object_or_404(Tecnologia, id=id)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tecnologia)
    if form.is_valid():
        form.save()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/edita_tecnologia.html', {'form': form, 'tecnologia': tecnologia})

@login_required
def tecnologia_apagar_view(request, id):
    if not e_gestor(request.user): raise PermissionDenied
    tecnologia = get_object_or_404(Tecnologia, id=id)
    if request.method == 'POST':
        tecnologia.delete()
    return redirect('portfolio:tecnologias')

# UCs
def ucs_view(request):
    ucs = UnidadeCurricular.objects.select_related('licenciatura').all()
    return render(request, 'portfolio/ucs.html', {'ucs': ucs})

# Competências
def competencias_view(request):
    competencias = Competencia.objects.all()
    return render(request, 'portfolio/competencias.html', {'competencias': competencias})

@login_required
def competencia_criar_view(request):
    if not e_gestor(request.user): raise PermissionDenied
    form = CompetenciaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:competencias')
    return render(request, 'portfolio/nova_competencia.html', {'form': form})

@login_required
def competencia_editar_view(request, id):
    if not e_gestor(request.user): raise PermissionDenied
    competencia = get_object_or_404(Competencia, id=id)
    form = CompetenciaForm(request.POST or None, instance=competencia)
    if form.is_valid():
        form.save()
        return redirect('portfolio:competencias')
    return render(request, 'portfolio/edita_competencia.html', {'form': form, 'competencia': competencia})

@login_required
def competencia_apagar_view(request, id):
    if not e_gestor(request.user): raise PermissionDenied
    competencia = get_object_or_404(Competencia, id=id)
    if request.method == 'POST':
        competencia.delete()
    return redirect('portfolio:competencias')

# Formações
def formacoes_view(request):
    formacoes = Formacao.objects.all()
    return render(request, 'portfolio/formacoes.html', {'formacoes': formacoes})

@login_required
def formacao_criar_view(request):
    if not e_gestor(request.user): raise PermissionDenied
    form = FormacaoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:formacoes')
    return render(request, 'portfolio/nova_formacao.html', {'form': form})

@login_required
def formacao_editar_view(request, id):
    if not e_gestor(request.user): raise PermissionDenied
    formacao = get_object_or_404(Formacao, id=id)
    form = FormacaoForm(request.POST or None, request.FILES or None, instance=formacao)
    if form.is_valid():
        form.save()
        return redirect('portfolio:formacoes')
    return render(request, 'portfolio/edita_formacao.html', {'form': form, 'formacao': formacao})

@login_required
def formacao_apagar_view(request, id):
    if not e_gestor(request.user): raise PermissionDenied
    formacao = get_object_or_404(Formacao, id=id)
    if request.method == 'POST':
        formacao.delete()
    return redirect('portfolio:formacoes')

# TFCs
def tfcs_view(request):
    tfcs = TFC.objects.all()
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})
