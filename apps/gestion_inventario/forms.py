from django import forms
from .models import Ubicacion, Compartimento, Categoria, Marca, ProductoGlobal


class AreaForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        # tipo_seccion y estacion no se exponen: tipo_seccion será 'AREA' y estacion se asigna desde la sesión
        # La imagen no se puede subir en la creación; sólo al editar
        fields = ['nombre', 'descripcion', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input_box__input fs_normal color_primario fondo_secundario', 'placeholder': 'Nombre del almacén'}),
            'descripcion': forms.Textarea(attrs={'class': 'input_box__input fs_normal color_primario fondo_secundario', 'rows': 3}),
            'direccion': forms.TextInput(attrs={'class': 'input_box__input fs_normal color_primario fondo_secundario', 'placeholder': 'Dirección (opcional)'}),
        }



class AreaEditForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre', 'descripcion', 'direccion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control fs_normal  color_primario fondo_secundario_variante border-0', 'rows': 3}),
            'direccion': forms.TextInput(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0'}),
        }



class CompartimentoForm(forms.ModelForm):
    class Meta:
        model = Compartimento
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0', 'placeholder': 'Nombre del compartimento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control fs_normal color_primario fondo_secundario_variante border-0', 'rows': 3}),
        }




class ProductoGlobalForm(forms.ModelForm):
    """
    Formulario para la creación de un nuevo Producto Global.
    La validación de marca/modelo vs. genérico se hereda del método .clean()
    que ya definimos en el modelo.
    """
    class Meta:
        model = ProductoGlobal
        fields = [
            'nombre_oficial', 
            'marca', 
            'modelo', 
            'categoria', 
            'descripcion_general', 
            'vida_util_recomendada_anos', 
            'imagen'
        ]
        widgets = {
            'nombre_oficial': forms.TextInput(attrs={'class': 'form-control fs_normal fondo_secundario color_primario'}),
            'marca': forms.Select(attrs={'class': 'form-select fs_normal fondo_secundario color_primario tom-select-creatable'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control fs_normal fondo_secundario color_primario'}),
            'categoria': forms.Select(attrs={'class': 'form-select fs_normal fondo_secundario color_primario'}),
            'descripcion_general': forms.Textarea(attrs={'class': 'form-control fs_normal fondo_secundario color_primario', 'rows': 3}),
            'vida_util_recomendada_anos': forms.NumberInput(attrs={'class': 'form-control fs_normal fondo_secundario color_primario'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control fs_normal fondo_secundario color_primario'}),
        }
        help_texts = {
            'nombre_oficial': 'Para productos genéricos (sin marca/modelo), usa un nombre descriptivo y único. Ej: "Guantes de Nitrilo Talla M".',
            'modelo': 'Si seleccionaste una marca, este campo es obligatorio.',
        }

    def __init__(self, *args, **kwargs):
        """
        Poblamos los QuerySets de los campos ForeignKey para que estén ordenados.
        """
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.order_by('nombre')
        self.fields['marca'].queryset = Marca.objects.order_by('nombre')