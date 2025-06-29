from django.shortcuts import render
from django.views import View

class MantenimientoInicioView(View):
    def get(self, request):
        return render(request, "gestion_mantenimiento/pages/home.html")