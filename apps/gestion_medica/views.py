from django.shortcuts import render
from django.views import View


class MedicoInicioView(View):
    '''Vista para ver la página principal del módulo'''
    def get(self, request):
        return render(request, "gestion_medica/pages/home.html")
    


class MedicoListaView(View):
    def get(self, request):
        return render(request, "gestion_medica/lista_voluntarios.html")



class MedicoVerView(View):
    def get(self, request):
        return render(request, "gestion_medica/ver_voluntario.html")



class MedicoModificarView(View):
    def get(self, request):
        return render(request, "gestion_medica/modificar_voluntario.html")