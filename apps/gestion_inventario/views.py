from django.shortcuts import render
from django.views import View


class InventarioInicioView(View):
    def get(self, request):
        return render(request, "gestion_inventario/pages/home.html")