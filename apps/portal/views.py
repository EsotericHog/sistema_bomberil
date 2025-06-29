from django.shortcuts import render
from django.views import View


class InicioView(View):
    def get(self, request):
        return render(request, "portal/pages/home.html")