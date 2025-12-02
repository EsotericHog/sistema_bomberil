# ==============================================================================
# LÓGICA DE COMPATIBILIDAD SANGUÍNEA (Donante -> Receptor)
# Esta es la base para determinar quién puede donar a quién.
# Se define como: {'TIPO_DONANTE': ['TIPO_RECEPTOR_1', 'TIPO_RECEPTOR_2', ...]}
# ==============================================================================
BLOOD_COMPATIBILITY = {
    'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'], # Donante Universal
    'O+': ['O+', 'A+', 'B+', 'AB+'],
    'A-': ['A-', 'A+', 'AB-', 'AB+'],
    'A+': ['A+', 'AB+'],
    'B-': ['B-', 'B+', 'AB-', 'AB+'],
    'B+': ['B+', 'AB+'],
    'AB-': ['AB-', 'AB+'],
    'AB+': ['AB+'], # Receptor Universal (solo puede donar a su mismo tipo)
}