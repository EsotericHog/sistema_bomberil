from django import template
from datetime import date

register = template.Library()

@register.filter(name='calculate_age')
def calculate_age(birth_date):
    """
    Recibe una fecha de nacimiento y devuelve la edad actual.
    """
    if not isinstance(birth_date, date):
        return 0 # O maneja el error como prefieras

    today = date.today()
    # Este cálculo simple pero robusto determina la edad correctamente.
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age