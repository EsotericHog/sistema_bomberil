from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.core.files.base import ContentFile
from PIL import Image

from .models import Usuario
from .funciones import recortar_y_redimensionar_avatar, generar_avatar_thumbnail
from apps.gestion_voluntarios.models import Voluntario



@receiver(pre_delete, sender=Usuario)
def eliminar_archivos_de_avatar(sender, instance, **kwargs):
    """
    Elimina todos los archivos del avatar al borrar el usuario.
    """
    if instance.avatar:
        instance.avatar.delete(save=False)

    if instance.avatar_thumb_small:
        instance.avatar_thumb_small.delete(save=False)
    if instance.avatar_thumb_medium:
        instance.avatar_thumb_medium.delete(save=False)




@receiver(post_save, sender=Usuario)
def crear_perfiles_automaticamente(sender, instance, created, **kwargs):
    """
    Crea Voluntario (HojaDeVida) y FichaMedica vacías automáticamente 
    cuando un nuevo Usuario es creado.
    """
    if created:
        Voluntario.objects.create(usuario=instance)
        # FichaMedica.objects.create(usuario=instance)