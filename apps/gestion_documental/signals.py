import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import generar_preview_documento
from .models import DocumentoHistorico

@receiver(post_save, sender=DocumentoHistorico)
def trigger_generar_preview(sender, instance, created, **kwargs):
    """
    Se ejecuta después de guardar.
    Lanza el procesamiento en un Hilo (Thread) separado para no bloquear al usuario.
    """
    if instance.archivo and not instance.preview_imagen:
        # En lugar de llamar a la función directamente, creamos un hilo
        task = threading.Thread(
            target=generar_preview_documento, 
            args=(instance,)
        )
        # Iniciamos el hilo (el código principal sigue sin esperar)
        task.start()