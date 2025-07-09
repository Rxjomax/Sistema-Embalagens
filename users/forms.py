# Ficheiro: users/forms.py

from django import forms
from django.contrib.auth.models import User, Group
from localflavor.br.forms import BRCPFField
from .models import Profile
from core.forms import RequiredFieldsMixin

class FormWithFormControl(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            current_class = widget.attrs.get('class', '')
            if 'form-control' not in current_class:
                widget.attrs['class'] = f'{current_class} form-control'.strip()

class UserCreationForm(RequiredFieldsMixin, FormWithFormControl):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Cargo")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    full_name = forms.CharField(label="Nome Completo", max_length=150, required=True)

    class Meta:
        model = User
        # --- ORDEM DOS CAMPOS ATUALIZADA ---
        fields = ['full_name', 'username', 'email', 'password', 'group', 'first_name', 'last_name']
        widgets = {
            'first_name': forms.HiddenInput(), # Escondido, preenchido por JS
            'last_name': forms.HiddenInput(), # Escondido, preenchido por JS
            'username': forms.TextInput(attrs={'placeholder': '(Sugerido)'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            user.groups.set([self.cleaned_data['group']])
        return user

class UserChangeForm(RequiredFieldsMixin, FormWithFormControl):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Cargo")
    class Meta:
        model = User
        # --- ORDEM DOS CAMPOS ATUALIZADA ---
        fields = ['first_name', 'last_name', 'username', 'email', 'group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.groups.exists():
            self.fields['group'].initial = self.instance.groups.first()

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.groups.set([self.cleaned_data['group']])
        return user

class ProfileForm(RequiredFieldsMixin, FormWithFormControl):
    cpf = BRCPFField(label="CPF", required=False)
    class Meta:
        model = Profile
        # --- ORDEM DOS CAMPOS ATUALIZADA ---
        fields = ['phone', 'cpf', 'code', 'photo']