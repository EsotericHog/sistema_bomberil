from django.shortcuts import render
from django.views import View


class MedicoInicioView(View):
    '''Vista para ver la página principal del módulo'''
    def get(self, request):
        return render(request, "gestion_medica/pages/home.html")
    


class MedicoCrearView(View):
    def get(self, request):
        return render(request, "gestion_medica/pages/crear_voluntario.html")



class MedicoListaView(View):
    def get(self, request):
        return render(request, "gestion_medica/pages/lista_voluntarios.html")



class MedicoVerView(View):
    def get(self, request):
        return render(request, "gestion_medica/pages/ver_voluntario.html")



class MedicoModificarView(View):
    def get(self, request):
        return render(request, "gestion_medica/pages/modificar_voluntario.html")
    
class MedicamentoCrearView(View):
    def get(self, request):
        return render(request, "gestion_medica/pages/crear_medicamento.html")
    
class MedicamentoListView(View):
    def get(self, request):
        return render(request, "gestion_medica/pages/lista_medicamentos.html")