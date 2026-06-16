from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from example.models import User, Instituicao, Comunidade, Mensagem

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

@login_required
def comunidades_view(request):
    search_query = request.GET.get('search', '').strip()
    comunidades = Comunidade.objects.select_related('administrador').prefetch_related('membros')
    if search_query:
        comunidades = comunidades.filter(
            Q(nome__icontains=search_query) |
            Q(descricao__icontains=search_query) |
            Q(administrador__username__icontains=search_query)
        )
    comunidades = comunidades.all()

    form = ComunidadeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comunidade = form.save(commit=False)
        comunidade.administrador = request.user
        comunidade.save()
        comunidade.membros.add(request.user)
        return redirect('comunidades')
    return render(request, 'frontend/comunidades.html', {
        'comunidades': comunidades,
        'form': form,
        'search_query': search_query,
    })

@login_required
def comunidade_detalhe_view(request, pk):
    comunidade = get_object_or_404(Comunidade, pk=pk)
    is_member = comunidade.membros.filter(pk=request.user.pk).exists()
    is_pending = comunidade.membros_pendentes.filter(pk=request.user.pk).exists()
    is_admin = request.user == comunidade.administrador
    is_muted = comunidade.is_muted(request.user)
    message_form = MensagemForm(request.POST or None)

    if request.method == 'POST':
        if 'join' in request.POST and not is_member and not is_pending:
            comunidade.request_membership(request.user)
            return redirect('comunidade_detalhe', pk=pk)

        if 'approve_member' in request.POST and is_admin:
            usuario_id = request.POST.get('user_id')
            usuario = get_object_or_404(User, pk=usuario_id)
            comunidade.approve_member(usuario)
            return redirect('comunidade_detalhe', pk=pk)

        if 'reject_member' in request.POST and is_admin:
            usuario_id = request.POST.get('user_id')
            usuario = get_object_or_404(User, pk=usuario_id)
            comunidade.reject_member(usuario)
            return redirect('comunidade_detalhe', pk=pk)

        if 'mute_member' in request.POST and is_admin:
            usuario_id = request.POST.get('user_id')
            usuario = get_object_or_404(User, pk=usuario_id)
            comunidade.mute_member(usuario)
            return redirect('comunidade_detalhe', pk=pk)

        if 'unmute_member' in request.POST and is_admin:
            usuario_id = request.POST.get('user_id')
            usuario = get_object_or_404(User, pk=usuario_id)
            comunidade.unmute_member(usuario)
            return redirect('comunidade_detalhe', pk=pk)

        if 'remove_member' in request.POST and is_admin:
            usuario_id = request.POST.get('user_id')
            usuario = get_object_or_404(User, pk=usuario_id)
            if usuario != comunidade.administrador:
                comunidade.membros.remove(usuario)
                comunidade.membros_silenciados.remove(usuario)
            return redirect('comunidade_detalhe', pk=pk)

        if 'send_message' in request.POST and is_member and not is_muted and message_form.is_valid():
            mensagem = message_form.save(commit=False)
            mensagem.comunidade = comunidade
            mensagem.autor = request.user
            mensagem.save()
            return redirect('comunidade_detalhe', pk=pk)

    mensagens = comunidade.mensagens.select_related('autor').all()
    pending_requests = comunidade.membros_pendentes.all() if is_admin else []
    muted_member_ids = list(comunidade.membros_silenciados.values_list('pk', flat=True))
    return render(request, 'frontend/comunidade_detalhe.html', {
        'comunidade': comunidade,
        'mensagens': mensagens,
        'is_member': is_member,
        'is_pending': is_pending,
        'is_admin': is_admin,
        'is_muted': is_muted,
        'pending_requests': pending_requests,
        'muted_member_ids': muted_member_ids,
        'message_form': message_form,
    })

def logout_view(request):
    logout(request)
    return redirect('login')



from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, ComunidadeForm, MensagemForm

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