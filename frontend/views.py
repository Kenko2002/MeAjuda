from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from example.models import Instituicao

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # Redireciona para a home após login
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})

@login_required
def home_view(request):
    # Obtém as tags do usuário logado
    user_tags = request.user.problemas.all()
    
    # Filtra instituições que tenham QUALQUER uma das tags do usuário
    # .distinct() evita duplicados se a instituição tiver mais de uma tag comum
    instituicoes = Instituicao.objects.filter(tags__in=user_tags).distinct()
    
    context = {
        'instituicoes': instituicoes,
        'user_tags': user_tags
    }
    return render(request, 'frontend/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')



from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'frontend/profile.html', {'form': form})