import sys
from django.conf import settings
from apps.gestion_usuarios.models import RegistroActividad

def core_registrar_actividad(request, verbo, objetivo=None, detalles=None, objetivo_repr=None):
    """
    Servicio central para registrar auditoría.
    Maneja fallos silenciosamente para no interrumpir al usuario.
    """
    try:
        # 1. Obtener la estación activa desde la sesión (Regla de Negocio)
        # [cite: 21] active_estacion_id se guarda en sesión al autenticarse
        estacion_id = request.session.get('active_estacion_id')
        
        # 2. Determinar el actor
        # Si es una tarea de sistema o cron, user podría ser None o no estar autenticado
        actor = request.user if (request.user and request.user.is_authenticated) else None

        # 3. Snapshot del objetivo (para cuando se elimine)
        if objetivo_repr:
            texto_final_objetivo = objetivo_repr
        else:
            texto_final_objetivo = str(objetivo) if objetivo else "Objeto no especificado o eliminado"

        # 4. Crear el registro
        RegistroActividad.objects.create(
            actor=actor,
            estacion_id=estacion_id, 
            verbo=verbo,
            objetivo_generico=objetivo,
            objetivo_repr=texto_final_objetivo,
            detalles=detalles or {}
        )
    except Exception as e:
        # En producción, esto debería ir a un log de errores (Sentry, CloudWatch, etc.)
        # Imprimimos en stderr para desarrollo, pero NO lanzamos la excepción hacia la vista.
        print(f"Error CRÍTICO (Silenciado) en Auditoría: {e}", file=sys.stderr)