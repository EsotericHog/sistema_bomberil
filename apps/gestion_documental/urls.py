from django.urls import path
from .views import DocumentalInicioView

app_name = 'gestion_documental'

urlpatterns = [
    # Página Inicial de la gestión documental
    path('', DocumentalInicioView.as_view(), name="ruta_inicio"),
]