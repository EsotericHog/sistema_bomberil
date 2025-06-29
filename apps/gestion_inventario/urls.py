from django.urls import path
from .views import *

urlpatterns = [
    # Página Inicial de la gestión de inventario
    path('', InventarioInicioView.as_view(), name="ruta_inventario_inicio"),
]