from django.urls import path
from .views import LoginView, LogoutView

app_name = "acceso"

urlpatterns = [
    path('login/', LoginView.as_view(), name="ruta_login"),
    path('logout/', LogoutView.as_view(), name="ruta_logout"),
]