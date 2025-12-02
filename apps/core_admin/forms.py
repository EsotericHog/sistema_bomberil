from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import Permission

from apps.gestion_inventario.models import Estacion, Comuna, ProductoGlobal, Marca, Categoria
from apps.gestion_usuarios.models import Usuario, Rol, Membresia
from apps.common.mixins import ImageProcessingFormMixin


class EstacionForm(ImageProcessingFormMixin, forms.ModelForm):
    class Meta:
        model = Estacion
        fields = ['nombre', 'descripcion', 'es_departamento', 'direccion', 'comuna', 'logo', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'es_departamento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Aplicar clases de Bootstrap + Tus clases de texto
        for field_name, field in self.fields.items():
            if field_name != 'es_departamento': # El checkbox tiene su propia clase
                # Aplicamos text-sm para un tamaño de fuente cómodo en inputs (1.4rem)
                field.widget.attrs['class'] = 'form-control text-sm'
        
        # 2. Optimizar el selector de Comunas (ordenar y mostrar región)
        self.fields['comuna'].queryset = Comuna.objects.select_related('region').order_by('region__nombre', 'nombre')
        
        # 3. Etiquetas personalizadas
        self.fields['comuna'].empty_label = "Seleccione una Comuna..."
    

    def save(self, commit=True):
        estacion = super().save(commit=False)
        
        # 1. Procesar IMAGEN
        self.process_image_upload(
            instance=estacion, 
            field_name='imagen',
            max_dim=(1024, 1024), 
            crop=False,
            image_prefix='estacion'
        )

        # 2. Procesar LOGO
        self.process_image_upload(
            instance=estacion, 
            field_name='logo',
            max_dim=(800, 800), 
            crop=True,
            image_prefix='estacion_logo'
        )

        # 3. Guardar
        if commit:
            estacion.save()
            
        return estacion




class ProductoGlobalForm(ImageProcessingFormMixin, forms.ModelForm):
    class Meta:
        model = ProductoGlobal
        fields = [
            'nombre_oficial', 'categoria', 'marca', 'modelo', 
            'gtin', 'vida_util_recomendada_anos', 'descripcion_general', 'imagen'
        ]
        widgets = {
            'descripcion_general': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describa las características técnicas principales...'}),
            'nombre_oficial': forms.TextInput(attrs={'placeholder': 'Ej: Hacha de Bombero Flathead'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Ej: G1, 4.5, AirPak...'}),
            # GTIN es un código, le agregamos la clase especial text-data-code
            'gtin': forms.TextInput(attrs={'placeholder': 'Código de barras / EAN', 'class': 'form-control text-sm text-data-code'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar estilos Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            # Si el widget ya tiene clases (como GTIN arriba), las conservamos y agregamos las generales si faltan
            current_classes = field.widget.attrs.get('class', '')
            
            if 'form-control' not in current_classes:
                # Si no tiene clase definida, aplicamos la estándar
                field.widget.attrs['class'] = 'form-control text-sm'
            else:
                # Si ya tiene (ej: GTIN), nos aseguramos que tenga text-sm
                if 'text-sm' not in current_classes:
                    field.widget.attrs['class'] += ' text-sm'

        # Mejorar la UX de los selectores
        self.fields['categoria'].empty_label = "Seleccione Categoría..."
        self.fields['marca'].empty_label = "Sin Marca (Genérico)"
        
        self.fields['vida_util_recomendada_anos'].label = "Vida Útil Estándar (Años)"


    def save(self, commit=True):
        producto = super().save(commit=False)
        
        self.process_image_upload(
            instance=producto, 
            field_name='imagen', 
            max_dim=(1024, 1024), 
            crop=False,
            image_prefix='producto'
        )

        if commit:
            producto.save()
            
        return producto




class UsuarioCreationForm(forms.ModelForm):
    """
    Formulario para crear usuarios nuevos con validación de contraseña.
    """
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        help_text="Mínimo 8 caracteres."
    )
    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

    class Meta:
        model = Usuario
        fields = ['rut', 'first_name', 'last_name', 'email', 'phone', 'is_active', 'is_staff']
        widgets = {
            # RUT es un identificador, usamos text-data-code
            'rut': forms.TextInput(attrs={'placeholder': '12.345.678-9', 'class': 'form-control text-sm text-data-code'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Ej: Juan'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ej: Pérez'}),
            'email': forms.EmailInput(attrs={'placeholder': 'juan.perez@bomberos.cl'}),
            'phone': forms.TextInput(attrs={'placeholder': '9 1234 5678', 'class': 'form-control text-sm text-data-code'}), # Teléfono también es dato numérico
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'rut': 'RUT (Identificador)',
            'is_active': 'Cuenta Activa',
            'is_staff': 'Es Staff (Acceso Admin)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estilos Bootstrap generales
        for field_name, field in self.fields.items():
            if field_name not in ['is_active', 'is_staff']: 
                # Preservar clases existentes (como en RUT o Phone)
                current_classes = field.widget.attrs.get('class', '')
                if 'form-control' not in current_classes:
                    field.widget.attrs['class'] = 'form-control text-sm'
                elif 'text-sm' not in current_classes:
                     field.widget.attrs['class'] += ' text-sm'

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if Usuario.objects.filter(rut=rut).exists():
            raise ValidationError("Ya existe un usuario registrado con este RUT.")
        return rut

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user




class UsuarioChangeForm(forms.ModelForm):
    """
    Formulario para EDITAR usuarios existentes.
    """
    class Meta:
        model = Usuario
        fields = ['rut', 'first_name', 'last_name', 'email', 'phone', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            # RUT Readonly y con fuente de datos
            'rut': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control text-sm text-data-code'}), 
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilos Bootstrap
        for field_name, field in self.fields.items():
            if field_name not in ['is_active', 'is_staff', 'is_superuser']:
                current_classes = field.widget.attrs.get('class', '')
                if 'form-control' not in current_classes:
                    field.widget.attrs['class'] = 'form-control text-sm'
                elif 'text-sm' not in current_classes:
                    field.widget.attrs['class'] += ' text-sm'
        
        # Aplicar text-data-code al teléfono también si se desea consistencia
        if 'phone' in self.fields:
             self.fields['phone'].widget.attrs['class'] += ' text-data-code'

        self.fields['is_superuser'].help_text = "<strong>¡Cuidado!</strong> Otorga acceso total al sistema y evita todas las restricciones de permisos."
        self.fields['rut'].help_text = "El identificador (RUT) no se puede modificar libremente para mantener la integridad histórica."




class AsignarMembresiaForm(forms.ModelForm):
    roles_seleccionados = forms.ModelMultipleChoiceField(
        queryset=Rol.objects.none(),
        # Agregamos text-sm al select múltiple
        widget=forms.SelectMultiple(attrs={'class': 'form-select text-sm', 'size': '8'}),
        label="Roles a Asignar",
        help_text="Mantén presionada la tecla Ctrl (o Cmd) para seleccionar múltiples roles."
    )

    class Meta:
        model = Membresia
        fields = ['usuario', 'estacion', 'fecha_inicio']
        widgets = {
            # Fecha y Selects con text-sm
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control text-sm text-data-code'}), # Fechas son datos
            'usuario': forms.Select(attrs={'class': 'form-select text-sm'}),
            'estacion': forms.Select(attrs={'class': 'form-select text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'estacion' in self.data:
            try:
                estacion_id = int(self.data.get('estacion'))
                self.fields['roles_seleccionados'].queryset = Rol.objects.filter(
                    Q(estacion__isnull=True) | Q(estacion_id=estacion_id)
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['roles_seleccionados'].queryset = self.instance.estacion.roles.all()

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        
        if usuario:
            otras_activas = Membresia.objects.filter(
                usuario=usuario, 
                estado='ACTIVO'
            ).exclude(pk=self.instance.pk)

            if otras_activas.exists():
                estacion_actual = otras_activas.first().estacion.nombre
                
                raise ValidationError(
                    f"OPERACIÓN DENEGADA: El usuario {usuario} ya se encuentra ACTIVO en la estación '{estacion_actual}'. "
                    "Debe finalizar esa membresía antes de asignarle una nueva."
                )
        
        return cleaned_data




class RolGlobalForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'permisos']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'permisos': forms.MultipleHiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar text-sm explícitamente
        self.fields['nombre'].widget.attrs['class'] = 'form-control text-sm'
        self.fields['descripcion'].widget.attrs['class'] = 'form-control text-sm'
        
        criterio_negocio = Q(codename__startswith='acceso_') | Q(codename__startswith='accion_')
        
        self.fields['permisos'].queryset = Permission.objects.filter(
            criterio_negocio
        ).select_related('content_type').order_by('content_type__app_label', 'codename')
        
        self.fields['permisos'].required = False




class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre'] 
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Rosenbauer, MSA, Motorola...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar text-sm
        self.fields['nombre'].widget.attrs['class'] = 'form-control text-sm'
        self.fields['nombre'].label = "Nombre de la Marca"




class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'codigo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Protección Personal'}),
            # Código es un dato corto/técnico -> text-data-code
            'codigo': forms.TextInput(attrs={'placeholder': 'Ej: EPP, MM, COM...', 'class': 'form-control text-sm text-data-code'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa qué tipo de insumos agrupa esta categoría...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estilos Bootstrap + Texto
        for field_name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            
            if 'form-control' not in current_classes:
                field.widget.attrs['class'] = 'form-control text-sm'
            else:
                 if 'text-sm' not in current_classes:
                    field.widget.attrs['class'] += ' text-sm'
        
        self.fields['codigo'].label = "Código Corto (Único)"
        self.fields['codigo'].help_text = "Identificador breve para reportes y etiquetas."