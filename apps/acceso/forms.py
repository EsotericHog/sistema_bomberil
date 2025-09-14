from django import forms


class FormularioLogin(forms.Form):
    correo = forms.EmailField(
        required=True, 
        widget=forms.TextInput(
            attrs={
                'name':'LoginInputCorreo',
                'class':'input_box__input fs_normal color_primario fondo_secundario_variante',
                'autocomplete':'off',
            }
        )
    )

    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'name':'LoginInputPassword',
                'class':'input_box__input fs_normal color_primario fondo_secundario_variante',
                'autocomplete':'off'
            }
        )
    )