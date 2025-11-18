from django import forms
from apps.gestion_inventario.models import Estacion, Comuna

class EstacionForm(forms.ModelForm):
    class Meta:
        model = Estacion
        fields = ['nombre', 'descripcion', 'es_departamento', 'direccion', 'comuna', 'logo', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'es_departamento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Aplicar clases de Bootstrap a todos los campos visibles
        for field_name, field in self.fields.items():
            if field_name != 'es_departamento': # El checkbox tiene su propia clase
                field.widget.attrs['class'] = 'form-control'
        
        # 2. Optimizar el selector de Comunas (ordenar y mostrar región)
        # [cite_start]Esto evita que salgan desordenadas. [cite: 11]
        self.fields['comuna'].queryset = Comuna.objects.select_related('region').order_by('region__nombre', 'nombre')
        
        # 3. Etiquetas personalizadas si hacen falta
        self.fields['comuna'].empty_label = "Seleccione una Comuna..."