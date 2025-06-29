from django.shortcuts import render, redirect
from django.views import View



class UsuarioInicioView(View):
    '''Vista para la página inicial de Gestión de Usuarios'''

    def get(self, request):
        return render(request, "gestion_usuarios/pages/home.html")



class UsuarioListaView(View):
    '''Vista para listar usuarios'''
    
    def get(self, request):
        pass



class UsuarioObtenerView(View):
    '''Vista para obtener el detalle de un usuario'''

    def get(self, request):
        pass



class UsuarioCrearView(View):
    '''Vista para crear usuarios'''

    def get(self, request):
        pass

    def post(self, request):
        pass



class UsuarioEditarView(View):
    '''Vista para editar usuarios'''

    def get(self, request):
        pass

    def post(self, request):
        pass



class UsuarioDesactivarView(View):
    '''Vista para desactivar usuarios'''

    def get(self, request):
        pass

    def post(self, request):
        pass



def alternar_tema_oscuro(request):
    current = request.session.get('dark_mode', False)
    request.session['dark_mode'] = not current
    return redirect(request.META.get('HTTP_REFERER', '/'))