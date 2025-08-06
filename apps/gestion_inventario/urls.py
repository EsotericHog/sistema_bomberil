from django.urls import path
from .views import *

app_name = 'gestion_inventario'

urlpatterns = [
    # Página Inicial de la gestión de inventario
    path('', InventarioInicioView.as_view(), name="ruta_inventario_inicio"),
    # Pruebas
    path('pruebas/', InventarioPruebasView.as_view(), name="ruta_inventario_pruebas"),
    # Obtener datos para gráfico de total existencias por categoría (API)
    path('existencias_por_categoria/', grafico_existencias_por_categoria, name="ruta_inventario_obtener_grafico_categoria"),
]