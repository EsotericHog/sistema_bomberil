from rest_framework.permissions import BasePermission
from apps.gestion_usuarios.models import Membresia


class CanUpdateUserProfile(BasePermission):
    """
    Permiso personalizado que verifica si un usuario puede modificar un perfil.
    El acceso se concede si se cumple ALGUNA de las siguientes condiciones:
    1. El usuario está modificando su propio perfil (es el dueño).
    2. El usuario tiene el permiso para modificar perfiles Y el usuario objetivo
       pertenece a la misma estación activa que el administrador.
    """
    
    # Permiso de Django necesario para que un admin pueda editar a otros.
    required_admin_permission = 'gestion_usuarios.change_user_personal_info'

    def has_object_permission(self, request, view, obj):
        # 'obj' es la instancia del Usuario que se intenta modificar.
        # 'request.user' es el usuario que está haciendo la petición.

        # Condición 1: ¿El usuario está editando su propio perfil?
        if obj == request.user:
            return True

        # Si no es su propio perfil, pasamos a la lógica de administrador.
        # Condición 2: ¿Es un administrador con los permisos y contexto correctos?
        
        # Primero, ¿tiene el permiso de Django para editar usuarios?
        if not request.user.has_perm(self.required_admin_permission):
            return False

        # Segundo, ¿tenemos una estación activa para el administrador?
        admin_station_id = request.session.get('active_estacion_id')
        if not admin_station_id:
            return False
            
        # Tercero, y más importante: ¿El usuario objetivo tiene una membresía
        # válida en la misma estación que el administrador?
        # (Esta es la lógica de tu UsuarioDeMiEstacionMixin, traducida a DRF).
        return Membresia.objects.filter(
            usuario=obj,
            estacion_id=admin_station_id,
            estado__in=[Membresia.Estado.ACTIVO, Membresia.Estado.INACTIVO]
        ).exists()