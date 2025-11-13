from django.shortcuts import render
from django.views import View


class DocumentalInicioView(View):
    template_name = "gestion_documental/pages/home.html"

    def get(self, request):
        return render(request, self.template_name)