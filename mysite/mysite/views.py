from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def e_gestor(user):
    return user.groups.filter(name='gestor-portfolio').exists()


@login_required
def projeto_criar_view(request):
    if not e_gestor(request.user):
        raise PermissionDenied




@login_required
def projeto_editar_view(request, id):
    if not e_gestor(request.user):
        raise PermissionDenied




@login_required
def projeto_apagar_view(request, id):
    if not e_gestor(request.user):
        raise PermissionDenied

