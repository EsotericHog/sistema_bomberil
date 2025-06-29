from django.urls import path
from .views import *

'''
FUNCIONALIDADES A DESARROLLAR EN EL MÓDULO "GESTIÓN MÉDICA"

_ Medicamentos (secundario): Listar, agregar, modificar y eliminar
_ Enfermedades (secundario): Listar, agregar, modificar y eliminar

_ Pacientes (primario):
    Lista
        campos por ver
    
    Ver paciente:
        información personal específica, imagen, teléfono primario, enfermedades, medicamentos y operaciones

    "Agregar paciente" no aplica aquí. Los voluntarios son ingresados en otro módulo
    
    Modificar paciente:
        - modificar información médica (grupo sang, presión art, altura, peso, etc.)
        - asignar enfermedades padecidas (varios)
        - asignar medicamentos (varios)
        - asignar operaciones quirúrgicas
    
_ Generar ficha médica en formato PDF
_ Exportar listado de pacientes (excel, .csv, etc.)
'''

urlpatterns = [
    # Página Inicial de la gestión médica
    path('', MedicoInicioView.as_view(), name="ruta_medico_inicio"),

    # Lista de pacientes (información médica de los voluntarios)
    path('lista/', MedicoListaView.as_view(), name="ruta_medico_lista"),

    # Ver información médica de un voluntario
    path('<int:id>/', MedicoVerView.as_view(), name="ruta_medico_ver"),

    # Modificar información médica de un voluntario
    path('<int:id>/editar', MedicoModificarView.as_view(), name="ruta_medico_modificar"),
]