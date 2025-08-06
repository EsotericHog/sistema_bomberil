from django.urls import path
from .views import *

app_name = "gestion_usuarios"

urlpatterns = [
    # Página Inicial de la gestión de usuarios
    path('', UsuarioInicioView.as_view(), name="ruta_usuarios_inicio"),

    # Lista de usuarios
    path('lista-usuarios/', UsuarioListaView.as_view(), name="ruta_usuarios_lista_usuarios"),

    # Ver detalle de usuario
    path('lista-usuarios/<int:id>/', UsuarioObtenerView.as_view(), name="ruta_usuarios_ver_usuario"),

    # Crear usuario
    path('crear-usuario/', UsuarioCrearView.as_view(), name="ruta_usuarios_crear_usuario"),

    # Modificar usuario
    path('editar-usuario/<int:id>/', UsuarioEditarView.as_view(), name="ruta_usuarios_editar_usuario"),
    
    # Desactivar usuario (No puede acceder al sistema)
    path('desactivar-usuario/<int:id>/', UsuarioDesactivarView.as_view(), name="ruta_usuarios_desactivar_usuario"),

    # Alternar tema oscuro
    path('alternar-tema-oscuro/', alternar_tema_oscuro, name='ruta_usuarios_alternar_tema'),
]