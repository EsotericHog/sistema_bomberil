# Sistema de Gestión para la Segunda Compañia de Bomberos de Iquique

## Descargar repositorio
Usa `git clone` para clonar el proyecto
```bash
git clone https://github.com/EsotericHog/sistema_bomberil.git
```

## Instalación para ejecución local (desarrollo)
Para ejecutar los siguientes comandos, **posiciónate en el directorio raíz del proyecto** usando tu terminal o CLI de preferencia


### Crear entorno virtual
Necesario para almacenar las dependencias únicamente del proyecto. Crea un entorno venv11 con el siguiente comando:
```bash
python -m venv .venv
```

### Activar entorno virtual
Antes de continuar, debemos entrar/activar el entorno virtual. Para eso, ejecuta el siguiente comando (en la raíz del proyecto):
```bash
.venv/Scripts/Activate.ps1
```
Estaremos dentro del entorno virtual si vemos `(.venv)` a la izquierda del Prompt en tu terminal. Si más adelante deseas salir del entorno virtual, cierra el terminal o usa el comando `deactivate` para salir correctamente. Ejecuta los siguientes comandos con el entorno virtual activado.


### Actualizar pip (opcional)
Actualiza el gestor de paquetes de pip del entorno virtual:
```bash
python.exe -m pip install --upgrade pip
```

### Instalar las librerías necesarias
Ejecuta el siguiente comando para instalar las dependencias del requirements.txt:
```bash
pip install -r requirements.txt
```

### Crear base de datos
Durante la fase de desarrollo utilizaremos MYSQL.

Debes crear la base de datos con el nombre indicado en `.env` en el valor de `DB_NAME`. Necesitas generar un entorno local de desarrollo. Para eso, utiliza algún software como Laragon o XAMPP. Esto te permitirá gestionar tus bases de datos locales.

Usa algún gestor de bases de datos como phpmyadmin o MySQL Workbench para crear la base de datos.


### Generar migraciones
Para generar las migraciones, ejecuta el siguiente comando:
```bash
python manage.py makemigrations
```


### Ejecutar migraciones
Para crear las tablas en la base de datos, ejecuta el siguiente comando:
```bash
python manage.py migrate
```


### Iniciar proyecto
```bash
python manage.py runserver localhost:8000
```