from django.apps import AppConfig


class GestionDocumentalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gestion_documental'
    verbose_name = 'Gestión Documental'

    def ready(self):
        import apps.gestion_documental.signals
