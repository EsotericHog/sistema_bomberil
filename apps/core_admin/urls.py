from django.urls import path
from .views import AdministracionInicioView, EstacionListView

app_name = 'core_admin'

urlpatterns = [
    # Página Inicial
    path('', AdministracionInicioView.as_view(), name="ruta_inicio"),

    # Lista de estaciones
    path('estaciones/', EstacionListView.as_view(), name='ruta_lista_estaciones'),

]