import os
from celery import Celery
from django.conf import settings

# 1. Establece el módulo de configuración de Django por defecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# 2. Carga la configuración desde settings.py usando el prefijo CELERY_
# Esto permite que en settings uses CELERY_BROKER_URL, etc.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 3. AUTO-DESCUBRIMIENTO DE TAREAS
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')