import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission

from .manager import CustomUserManager
from apps.utilidades.manejar_imagenes import generar_ruta_subida_local_avatar
from apps.gestion_inventario.models import Estacion


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True, verbose_name="correo electrónico")
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    rut = models.CharField(max_length=15, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    birthdate = models.DateField(null=True, blank=True, verbose_name="Fecha Nacimiento")
    phone = models.CharField(max_length=9, null=True, blank=True, verbose_name="Teléfono")
    avatar = models.ImageField(upload_to=generar_ruta_subida_local_avatar, null=True, blank=True)
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Estación correspondiente")
    
    # Campos automáticos de fecha
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS= ["first_name", "last_name"]

    objects= CustomUserManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"


    def __str__(self):
        return self.email
    

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'