from django.urls import path
from .views import *

app_name = "api"

urlpatterns = [
    # Alternar tema oscuro
    path('alternar-tema-oscuro/', alternar_tema_oscuro, name='ruta_alternar_tema'),
    path('buscar-usuario-para-agregar', BuscarUsuarioAPIView.as_view(), name='ruta_buscar_usuario'),
]