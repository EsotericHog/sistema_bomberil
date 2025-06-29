from pathlib import Path
import os
import environ


# Crea rutas dentro del proyecto de esta forma: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de variables de entorno
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Aplicaciones predeterminadas de Django
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# Aplicaciones del proyecto
PROJECT_APPS = [
    'apps.utilidades',
    'apps.gestion_usuarios',
    'apps.gestion_inventario',
    'apps.gestion_mantenimiento',
    'apps.gestion_voluntarios',
    'apps.gestion_medica',
    'apps.portal'
]
# Aplicaciones de terceros
THIRD_PARTY_APPS = [
    'jazzmin'
]
INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Base de datos
DATABASES = {
    "default": {
        "ENGINE": env.str('DB_ENGINE'),
        "NAME": env.str('DB_NAME'),
        "USER": env.str('DB_USER'),
        "PASSWORD": env.str('DB_PASSWORD'),
        "HOST": env.str('DB_HOST'),
        "PORT": env.str('DB_PORT'),
        "TEST": {
            "NAME": "mytestdatabase",
        },
    },
}


# Validaciones de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
STATIC_URL = 'static/'
# Directorio global de archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Tipo de campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Modelo personalizado de usuarios
AUTH_USER_MODEL = "gestion_usuarios.Usuario"