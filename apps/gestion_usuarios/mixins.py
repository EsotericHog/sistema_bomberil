from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Membresia

class UsuarioDeMiEstacionMixin(AccessMixin):
    """
    Mixin que verifica que el usuario al que se intenta acceder
    pertenece a la misma estación que el usuario logueado.
    """
    def dispatch(self, request, *args, **kwargs):
        # Primero, asegúrate de que el usuario esté logueado
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Obtiene el ID de la estación del usuario que hace la petición
        estacion_actual_id = request.session.get('active_estacion_id')
        
        # Obtiene el ID del usuario que se quiere ver desde la URL
        usuario_a_ver_id = kwargs.get('id')

        # La validación clave:
        # ¿Existe una membresía activa para este usuario EN MI estación?
        es_miembro_valido = Membresia.objects.filter(
            usuario_id=usuario_a_ver_id,
            estacion_id=estacion_actual_id,
            estado__in=['ACTIVO', 'INACTIVO']
        ).exists()

        if not es_miembro_valido:
            # Si no existe, lanzamos un error 404 (No Encontrado).
            # Es más seguro que un 403 (Prohibido), ya que no revela
            # que el usuario existe.
            raise Http404("No se encontró el usuario en esta estación.")

        # Si la validación pasa, permite que la vista continúe.
        return super().dispatch(request, *args, **kwargs)