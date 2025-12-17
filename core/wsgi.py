import os
import warnings
from django.core.wsgi import get_wsgi_application

# Ignorar por el módulo que causa el ruido (user_sessions)
warnings.filterwarnings("ignore", module="user_sessions")


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
