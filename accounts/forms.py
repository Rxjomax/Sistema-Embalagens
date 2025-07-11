# Ficheiro: accounts/forms.py

from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    """
    Um formulário de login customizado que aplica os estilos corretos
    e ajusta os placeholders para o nosso novo design.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campo de usuário/email
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'voce@exemplo.com'
        })

        # Campo de senha
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '********'
        })