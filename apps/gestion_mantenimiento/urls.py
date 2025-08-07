from django.urls import path
from .views import *

app_name = 'gestion_mantenimiento'

urlpatterns = [
    # Página Inicial de la gestión de inventario
    path('', MantenimientoInicioView.as_view(), name="ruta_inicio"),
]