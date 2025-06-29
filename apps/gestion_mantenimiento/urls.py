from django.urls import path
from .views import *

urlpatterns = [
    # Página Inicial de la gestión de inventario
    path('', MantenimientoInicioView.as_view(), name="ruta_mantenimiento_inicio"),
]