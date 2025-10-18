from django.urls import path
from .views import *

app_name = 'gestion_inventario'

urlpatterns = [
    # Página Inicial de la gestión de inventario
    path('', InventarioInicioView.as_view(), name="ruta_inicio"),
    # Pruebas
    path('pruebas/', InventarioPruebasView.as_view(), name="ruta_pruebas"),
    # Obtener datos para gráfico de total existencias por categoría (API)
    path('existencias_por_categoria/', grafico_existencias_por_categoria, name="ruta_obtener_grafico_categoria"),

    # Lista de áreas
    path('areas/', AreaListaView.as_view(), name="ruta_lista_areas"),
    # Lista de compartimentos
    path('compartimentos/', CompartimentoListaView.as_view(), name='ruta_lista_compartimentos'),
    # Crear área
    path('areas/crear/', AreaCrearView.as_view(), name="ruta_crear_area"),
    # Gestionar detalle de un área
    path('areas/<int:ubicacion_id>/gestionar/', AreaDetalleView.as_view(), name='ruta_gestionar_area'),
    # Crear compartimento para un área
    path('areas/<int:ubicacion_id>/compartimentos/crear/', CompartimentoCrearView.as_view(), name='ruta_crear_compartimento'),
    # Editar área
    path('areas/<int:ubicacion_id>/editar/', AreaEditarView.as_view(), name='ruta_editar_area'),
]