from django import forms
from .models import Seccion


class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Seccion
        # tipo_seccion y estacion no se exponen: tipo_seccion será 'AREA' y estacion se asigna desde la sesión
        # La imagen no se puede subir en la creación; sólo al editar
        fields = ['nombre', 'descripcion', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input_box__input fs_normal color_primario fondo_secundario', 'placeholder': 'Nombre del almacén'}),
            'descripcion': forms.Textarea(attrs={'class': 'input_box__input fs_normal color_primario fondo_secundario', 'rows': 3}),
            'direccion': forms.TextInput(attrs={'class': 'input_box__input fs_normal color_primario fondo_secundario', 'placeholder': 'Dirección (opcional)'}),
        }


class CompartimentoForm(forms.ModelForm):
    class Meta:
        model = __import__('apps.gestion_inventario.models', fromlist=['Compartimento']).Compartimento
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0', 'placeholder': 'Nombre del compartimento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0', 'rows': 3}),
        }


class AlmacenEditForm(forms.ModelForm):
    class Meta:
        model = __import__('apps.gestion_inventario.models', fromlist=['Seccion']).Seccion
        fields = ['nombre', 'descripcion', 'direccion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control fs_normal  color_primario fondo_secundario_variante border-0', 'rows': 3}),
            'direccion': forms.TextInput(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0'}),
        }
