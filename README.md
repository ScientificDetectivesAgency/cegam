# Visor Geográfico Costero - Quintana Roo

Este proyecto es un visualizador geográfico basado en Django, Leaflet y PostGIS para el diagnóstico y monitoreo de la línea de costa.

## Inicio Rápido

### 1. Requisitos
- Python 3.10+
- PostgreSQL 15+ con extensión PostGIS.
- OSGeo4W (para soporte GDAL/GEOS en Windows).

### 2. Instalación
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Base de Datos
1. Crear base de datos `costas`.
2. Habilitar extensión: `CREATE EXTENSION postgis;`
3. Restaurar respaldo: `pg_restore -U postgres -d costas -v playas.tar`

### 4. Ejecución
```bash
python manage.py migrate
python manage.py runserver
```

Acceso al visor: **http://127.0.0.1:8000/mapa/**

## Documentación Completa
Para instrucciones detalladas de instalación y despliegue en producción, consulte el [Manual de Instalación](MANUAL_INSTALACION.md).
