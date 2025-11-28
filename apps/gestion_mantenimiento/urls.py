from django.urls import path
from .views import (
    MantenimientoInicioView,
    PlanMantenimientoListView,
    PlanMantenimientoCrearView,
    PlanMantenimientoGestionarView,
    PlanMantenimientoEditarView,
    PlanMantenimientoEliminarView,
    OrdenMantenimientoListView,
    OrdenCorrectivaCreateView,
    OrdenMantenimientoDetalleView
)

app_name = 'gestion_mantenimiento'

urlpatterns = [
    # Página Inicial de la gestión de inventario
    path('', MantenimientoInicioView.as_view(), name="ruta_inicio"),


    # --- Gestión de Planes ---
    
    # 1. Lista de todos los planes de mantenimiento
    path('planes/', PlanMantenimientoListView.as_view(), name='ruta_lista_planes'),
    
    # 2. Formulario para crear un nuevo plan
    path('planes/crear/', PlanMantenimientoCrearView.as_view(), name='ruta_crear_plan'),
    
    # 3. Vista de "Gestionar" (Detalle) de un plan. 
    #    Aquí es donde se verán los activos asignados y se podrán añadir/quitar.
    path('planes/<int:pk>/gestionar/', PlanMantenimientoGestionarView.as_view(), name='ruta_gestionar_plan'),
    
    # 4. Formulario para editar los datos de un plan (nombre, trigger, frecuencia)
    path('planes/<int:pk>/editar/', PlanMantenimientoEditarView.as_view(), name='ruta_editar_plan'),
    
    # 5. Vista de confirmación para eliminar un plan
    path('planes/<int:pk>/eliminar/', PlanMantenimientoEliminarView.as_view(), name='ruta_eliminar_plan'),


    # === GESTIÓN DE ÓRDENES DE TRABAJO ===

    # 1. Listado de Órdenes (Dashboard Operativo)
    path('ordenes/', OrdenMantenimientoListView.as_view(), name='ruta_lista_ordenes'),

    # 2. Crear Orden Correctiva (Sin plan previo)
    path('ordenes/nueva-correctiva/', OrdenCorrectivaCreateView.as_view(), name='ruta_crear_orden_correctiva'),

    # 3. Espacio de Trabajo / Ejecución
    # Usamos 'gestionar' para mantener consistencia con la nomenclatura de Planes
    path('ordenes/<int:pk>/gestionar/', OrdenMantenimientoDetalleView.as_view(), name='ruta_gestionar_orden'),
]
