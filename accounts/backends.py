# Ficheiro: accounts/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameBackend(ModelBackend):
    """
    Backend de autenticação customizado que permite login com email ou nome de usuário.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        # Tenta encontrar um usuário pelo email primeiro.
        try:
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            # Se não encontrar pelo email, tenta pelo nome de usuário.
            try:
                user = UserModel.objects.get(username__iexact=username)
            except UserModel.DoesNotExist:
                # Se não encontrar por nenhum dos dois, a autenticação falha.
                UserModel().set_password(password) # Previne "timing attacks"
                return None
        
        # Se um usuário foi encontrado, verifica a senha.
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None