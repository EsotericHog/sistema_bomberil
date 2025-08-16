from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Usuario



class FormularioCrearUsuario(forms.Form):
    correo = forms.EmailField(
        required=True, 
        widget=forms.TextInput(
            attrs={
                'id':'LoginInputCorreo',
                'class':'input_box__input fs_normal color_primario fondo_secundario',
                'autocomplete':'off',
            }
        )
    )
    nombre = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={
                'id':'UsuarioInputNombre',
                'class':'input_box__input fs_normal color_primario fondo_secundario',
                'autocomplete':'off',
            }
        )
    )
    apellido = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={
                'id':'UsuarioInputApellido',
                'class':'input_box__input fs_normal color_primario fondo_secundario',
                'autocomplete':'off',
            }
        )
    )
    rut = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={
                'id':'UsuarioInputRut',
                'class':'input_box__input fs_normal color_primario fondo_secundario',
                'autocomplete':'off',
            }
        )
    )
    fecha_nacimiento = forms.DateField(
        required=False, 
        widget=forms.DateInput(
            attrs={
                'type':'date',
                'id':'UsuarioInputFechaNacimiento',
                'class':'input_box__input fs_normal color_primario fondo_secundario',
                'autocomplete':'off',
            }
        )
    )
    telefono = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={
                'id':'UsuarioInputTelefono',
                'class':'input_box__input fs_normal color_primario fondo_secundario',
                'autocomplete':'off',
            }
        )
    )
    avatar = forms.ImageField(
        required=False, 
        widget=forms.ClearableFileInput(
            attrs={
                'id':'UsuarioInputAvatar',
                'class':'input_box__input-file fs_normal color_primario fondo_secundario',
                'autocomplete':'off',
            }
        )
    )



class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para crear nuevos usuarios. Hereda de UserCreationForm
    y se adapta al modelo Usuario personalizado.
    """
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Incluye los campos que quieres en el formulario de creación.
        # El password se maneja automáticamente por UserCreationForm.
        fields = ('email', 'first_name', 'last_name', 'birthdate')

    
    # --- MÉTODO DE DEPURACIÓN AÑADIDO ---
    def is_valid(self):
        # Llama al is_valid() original primero
        valid = super().is_valid()

        # Si el formulario no es válido, imprime los errores en la consola
        if not valid:
            print("--- ERRORES DE VALIDACIÓN DEL FORMULARIO ---")
            print(self.errors.as_json())
            print("-----------------------------------------")
            
        return valid



class CustomUserChangeForm(UserChangeForm):
    """
    Formulario para modificar usuarios existentes. Hereda de UserChangeForm
    y se adapta al modelo Usuario personalizado.
    """
    class Meta:
        model = Usuario
        # __all__ es una opción, pero es mejor ser explícito con los campos.
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')