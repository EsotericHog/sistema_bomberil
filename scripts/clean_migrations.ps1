# -----------------------------------------------------------------
# Script: clean_migrations.ps1
# Descripción: ELIMINA caché y archivos de migración.
# Nota: No crea nuevas migraciones ni toca la base de datos.
# -----------------------------------------------------------------

$ErrorActionPreference = "Stop"

Write-Host "🧹 Iniciando limpieza de archivos..." -ForegroundColor Cyan

# 1. LIMPIAR CACHÉ (.pyc y __pycache__)
Write-Host " -> Eliminando caché de Python..."
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | 
    Where-Object { $_.FullName -notlike "*\.venv\*" } | 
    Remove-Item -Recurse -Force

Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" | 
    Where-Object { $_.FullName -notlike "*\.venv\*" } | 
    Remove-Item -Force

# 2. BORRAR MIGRACIONES (Respetando __init__.py)
Write-Host " -> Eliminando archivos de migración..."
Get-ChildItem -Path . -Recurse -File -Filter "*.py" | Where-Object { 
    $_.FullName -notlike "*\.venv\*" -and      # Ignorar entorno virtual
    $_.DirectoryName -like "*migrations*" -and # Solo carpetas migrations
    $_.Name -ne "__init__.py"                  # NUNCA borrar __init__.py
} | Remove-Item -Force

Write-Host "✅ ¡Limpieza completada! No quedan migraciones (excepto __init__.py)." -ForegroundColor Green