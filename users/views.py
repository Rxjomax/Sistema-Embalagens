# Ficheiro: users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserCreationForm, UserChangeForm, ProfileForm
from .models import Profile

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

# ==========================================================
# ========= VIEW DE CRIAÇÃO CORRIGIDA ABAIXO =========
# ==========================================================
def user_create_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f"Usuário '{user.username}' criado com sucesso!")
            return redirect('users:user_list')
        else:
            # Se o formulário for inválido, mostra uma mensagem de erro
            messages.error(request, 'Por favor, corrija os erros de validação abaixo.')
    else:
        # Para um GET, cria formulários em branco
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    # O contexto agora é montado aqui, servindo tanto para o GET quanto para um POST inválido
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': 'Adicionar Novo Usuário'
    }
    return render(request, 'users/user_form.html', context)

# ==========================================================
# ========= VIEW DE EDIÇÃO CORRIGIDA ABAIXO =========
# ==========================================================
def user_update_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Usuário '{user.username}' atualizado com sucesso!")
            return redirect('users:user_list')
        else:
            messages.error(request, 'Por favor, corrija os erros de validação abaixo.')
    else:
        user_form = UserChangeForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': f'Editando Usuário: {user.username}',
        'is_edit_form': True
    }
    return render(request, 'users/user_form.html', context)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')

    def form_valid(self, form):
        messages.success(self.request, "Usuário excluído com sucesso!")
        return super().form_valid(form)