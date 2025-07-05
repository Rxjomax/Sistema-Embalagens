# Ficheiro: users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Permission
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import UserCreationForm, UserChangeForm, ProfileForm
from .models import Profile

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_staff

@staff_member_required
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
            messages.error(request, 'Por favor, corrija os erros de validação abaixo.')
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': 'Adicionar Novo Usuário'
    }
    return render(request, 'users/user_form.html', context)

@staff_member_required
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

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')
    def test_func(self):
        return self.request.user.is_staff
    def form_valid(self, form):
        messages.success(self.request, "Usuário excluído com sucesso!")
        return super().form_valid(form)

class UserPermissionsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    
    def get(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)
        user_permissions = target_user.user_permissions.all()
        all_permissions = Permission.objects.all().select_related('content_type').order_by('content_type__app_label', 'codename')
        context = {
            'target_user': target_user,
            'user_permissions_pks': [p.pk for p in user_permissions],
            'all_permissions': all_permissions,
        }
        return render(request, 'users/user_permissions.html', context)

    def post(self, request, user_id):
        target_user = get_object_or_404(User, pk=user_id)
        permission_ids = request.POST.getlist('permissions')
        selected_permissions = Permission.objects.filter(pk__in=permission_ids)
        target_user.user_permissions.set(selected_permissions)
        messages.success(request, f"Permissões do usuário {target_user.username} atualizadas com sucesso!")
        return redirect('users:user_list')