import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class BomberilPasswordValidator:
    """
    Validador de complejidad robusta para el sistema de Bomberos.
    Exige:
    - 1 Mayúscula
    - 1 Minúscula
    - 1 Número
    - 1 Caracter Especial
    """

    def validate(self, password, user=None):
        # 1. Verificar Mayúscula
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper',
            )

        # 2. Verificar Minúscula
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra minúscula."),
                code='password_no_lower',
            )

        # 3. Verificar Dígito
        if not re.search(r'\d', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un número."),
                code='password_no_number',
            )

        # 4. Verificar Símbolo
        # Lista segura de símbolos (OWASP recommendation)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un caracter especial (ej: ! @ # $ %)."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe tener al menos una letra mayúscula, una minúscula, "
            "un número y un caracter especial."
        )