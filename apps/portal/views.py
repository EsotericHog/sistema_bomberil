from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin



class InicioView(LoginRequiredMixin, View):

    template_name = "portal/pages/home.html"

    def get(self, request):
        return render(request, self.template_name)