from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ubicacion, Compartimento

@receiver(post_save, sender=Ubicacion)
def crear_compartimento_general(sender, instance, created, **kwargs):
    """
    Signal que se activa después de guardar una Ubicacion.
    
    Si la Ubicacion es nueva (created=True), crea automáticamente
    un compartimento hijo llamado "General".
    """
    if created:
        Compartimento.objects.create(
            nombre="General",
            descripcion="Compartimento principal o área general de esta ubicación. Usar para ítems que no están en una gaveta o estante específico.",
            ubicacion=instance
        )