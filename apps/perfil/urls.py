from django.urls import path
from .views import VerPerfilView, EditarPerfilView, CambiarContrasenaView

app_name = 'perfil'

urlpatterns = [
    # URL para ver el perfil del usuario logueado
    path('', VerPerfilView.as_view(), name='ver'),
    
    # URL para editar la información del perfil
    path('editar/', EditarPerfilView.as_view(), name='editar'),
    
    # URL para el formulario de cambio de contraseña
    path('cambiar-contrasena/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
]