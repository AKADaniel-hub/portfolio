from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import MagicLink


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': 'Credenciais inválidas.'})

    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    return render(request, 'accounts/logout_confirm.html')





def magic_link_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            magic = MagicLink.objects.create(user=user)
            link = request.build_absolute_uri(f'/accounts/magic/{magic.token}/')

            send_mail(
                subject='O teu link de acesso',
                message=f'Clica aqui para entrares: {link}',
                from_email='noreply@portfolio.com',
                recipient_list=[email],
            )
            return render(request, 'accounts/magic_link_enviado.html', {'email': email})
        except User.DoesNotExist:
            return render(request, 'accounts/magic_link_request.html', {
                'error': 'Não existe nenhuma conta com esse email.'
            })

    return render(request, 'accounts/magic_link_request.html')


def magic_link_verify_view(request, token):
    try:
        magic = MagicLink.objects.get(token=token, usado=False)
        # expira ao fim de 15 minutos
        if magic.criado_em < timezone.now() - timedelta(minutes=15):
            return render(request, 'accounts/magic_link_expirado.html')

        magic.usado = True
        magic.save()
        login(request, magic.user)
        return redirect('portfolio:index')

    except MagicLink.DoesNotExist:
        return render(request, 'accounts/magic_link_expirado.html')