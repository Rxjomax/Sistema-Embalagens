from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    cpf = models.CharField(max_length=14, blank=True, unique=True, null=True, verbose_name="CPF")
    # Novo campo para a foto de perfil
    photo = models.ImageField(upload_to='users_photos/', null=True, blank=True, verbose_name="Foto de Perfil")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return self.user.username
