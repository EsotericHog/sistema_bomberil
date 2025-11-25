from django.urls import path
from .views import (
    alternar_tema_oscuro,
    BuscarUsuarioAPIView, 
    ActualizarAvatarUsuarioView, 
    ComunasPorRegionAPIView, 
    GraficoEstadosInventarioView, 
    GraficoExistenciasCategoriaView,
    ProductoGlobalSKUAPIView,
    AnadirProductoLocalAPIView
)

app_name = "api"

urlpatterns = [
    # Alternar tema oscuro
    path('alternar-tema-oscuro/', alternar_tema_oscuro, name='ruta_alternar_tema'),


    # --- USUARIOS ---
    # Buscar usuario para agregarlo a la estación
    path('gestion_usuarios/buscar-usuario-para-agregar', BuscarUsuarioAPIView.as_view(), name='ruta_buscar_usuario'),
    # Modificar avatar
    path('gestion_usuarios/usuarios/<uuid:id>/editar-avatar/', ActualizarAvatarUsuarioView.as_view(), name="ruta_editar_avatar_usuario"),


    # --- INVENTARIO ---
    # Obtener comunas por región
    path('gestion_inventario/comunas-por-region/<int:region_id>/', ComunasPorRegionAPIView.as_view(), name='comunas_por_region'),
    # Obtener gráfico de existencias por categoría
    path('gestion_inventario/existencias-por-categoria/', GraficoExistenciasCategoriaView.as_view(), name="ruta_obtener_grafico_categoria"),
    # Obtener gráfico existencias por estado
    path('gestion_inventario/existencias-por-estado/', GraficoEstadosInventarioView.as_view(), name="ruta_grafico_estado"),
    # Obtener detalle de producto global y SKU sugerido
    path('gestion_inventario/detalle-existencia/<int:pk>/', ProductoGlobalSKUAPIView.as_view(), name="api_get_producto_global_sku"),
    # Agregar producto al catálogo local
    path('gestion_inventario/anadir-producto-local/', AnadirProductoLocalAPIView.as_view(), name="api_anadir_producto_local")


    # --- APP ---
]