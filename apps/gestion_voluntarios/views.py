from django.shortcuts import render
from django.views import View


# Página Inicial
class VoluntariosInicioView(View):
    def get(self, request):
        return render(request, "gestion_voluntarios/pages/home.html")
    

# Lista de voluntarios
class VoluntariosListaView(View):
    def get(self, request):
        #código
        return render(request, "gestion_voluntarios/pages/lista_voluntarios.html")


# Crear voluntario
class VoluntariosCrearView(View):
    def get(self, request):
        return render(request, "gestion_voluntarios/pages/crear_voluntario.html")

    def post(self, request):
        # Lógica para guardar voluntario (más adelante)
        return render(request, "gestion_voluntarios/pages/crear_voluntario.html")


# Ver voluntario
class VoluntariosVerView(View):
    def get(self, request, id):
        return render(request, "gestion_voluntarios/pages/ver_voluntario.html")


# Editar voluntario
class VoluntariosModificarView(View):
    def get(self, request, id):
        return render(request, "gestion_voluntarios/pages/modificar_voluntario.html")

    def post(self, request, id):
        # Lógica para actualizar voluntario
        return render(request, "gestion_voluntarios/pages/modificar_voluntario.html")


# Eliminar voluntario
class VoluntariosEliminarView(View):
    def get(self, request, id):
        return render(request, "gestion_voluntarios/pages/eliminar_voluntario.html")

    def post(self, request, id):
        # Lógica para eliminar voluntario
        return render(request, "gestion_voluntarios/pages/eliminar_voluntario.html")



# GESTIÓN DE CARGOS Y PROFESIONES

# Lista de cargos y profesiones
class CargosListaView(View):
    def get(self, request):
        return render(request, "gestion_voluntarios/pages/lista_cargos_profes.html")

# Crear profesion
class ProfesionesCrearView(View):
    def get(self, request):
        return render(request, "gestion_voluntarios/pages/crear_profesion.html")

    def post(self, request):
        # Lógica para guardar profesion
        return render(request, "gestion_voluntarios/pages/crear_profesion.html")


# Editar profesion
class ProfesionesModificarView(View):
    def get(self, request, id):
        return render(request, "gestion_voluntarios/pages/modificar_profesion.html")

    def post(self, request, id):
        # Lógica para actualizar profesion
        return render(request, "gestion_voluntarios/pages/modificar_profesion.html")


# Eliminar profesion
class ProfesionesEliminarView(View):
    def get(self, request, id):
        return render(request, "gestion_voluntarios/pages/eliminar_profesion.html")

    def post(self, request, id):
        # Lógica para eliminar profesion
        return render(request, "gestion_voluntarios/pages/eliminar_profesion.html")

# Crear cargo
class CargosCrearView(View):
    def get(self, request):
        return render(request, "gestion_voluntarios/pages/crear_cargo.html")

    def post(self, request):
        # Lógica para guardar cargo
        return render(request, "gestion_voluntarios/pages/crear_cargo.html")


# Editar cargo
class CargosModificarView(View):
    def get(self, request, id):
        return render(request, "gestion_voluntarios/pages/modificar_cargo.html")

    def post(self, request, id):
        # Lógica para actualizar cargo
        return render(request, "gestion_voluntarios/pages/modificar_cargo.html")


# Eliminar cargo
class CargosEliminarView(View):
    def get(self, request, id):
        return render(request, "gestion_voluntarios/pages/eliminar_cargo.html")

    def post(self, request, id):
        # Lógica para eliminar cargo
        return render(request, "gestion_voluntarios/pages/eliminar_cargo.html")
    

# MODULO DE REPORTES EXPORTAR Y GENERAR HOJA DE VIDA

# Generar hoja de vida del voluntario
class HojaVidaView(View):
    def get(self, request):
        return render(request, "gestion_voluntarios/pages/hoja_vida.html")

# Exportar listado 
class ExportarListadoView(View):
    def get(self, request):
        return render(request, "gestion_voluntarios/pages/exportar_listado.html")
