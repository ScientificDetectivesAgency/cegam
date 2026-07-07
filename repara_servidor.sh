#!/bin/bash
# Script de Reparación Automática para Geotlalli (Linux Server)
# Ejecutar como usuario 'root' en: /var/www/geotlalli

set -e

echo "================================================================="
echo "   REPARADOR AUTOMÁTICO DE IMPLEMENTACIÓN - GEOTLALLI (LINUX)   "
echo "================================================================="

# 1. Definir rutas y verificar ubicación
PROJECT_DIR="/var/www/geotlalli"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERROR: El directorio $PROJECT_DIR no existe."
    exit 1
fi

cd "$PROJECT_DIR"
echo "[1/8] Directorio verificado: $(pwd)"
echo "[1/8] Ejecutando como usuario: $(whoami)"

# 2. Corregir saltos de línea Windows (CRLF) a formato Unix (LF)
echo "[2/8] Corrigiendo saltos de línea CRLF en archivos .py y .txt..."
find . -type f -name "*.py" -exec sed -i 's/\r$//' {} +
find . -type f -name "*.txt" -exec sed -i 's/\r$//' {} +
if [ -f manage.py ]; then
    sed -i 's/\r$//' manage.py
    chmod +x manage.py
fi

# 3. Eliminar y recrear un Entorno Virtual NATIVO de Linux
echo "[3/8] Reconstruyendo entorno virtual nativo..."
rm -rf venv
python3 -m venv venv
source venv/bin/activate

echo "[3/8] Instalando/actualizando pip, setuptools y wheel..."
pip install --upgrade pip setuptools wheel

echo "[3/8] Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt
pip install gunicorn

# 4. Probar Django y dependencias localmente en la terminal
echo "[4/8] Probando inicialización de Django y conexión a base de datos..."
if python manage.py check; then
    echo "✔ Django inicializó correctamente y pasó todos los chequeos locales."
else
    echo "❌ ERROR: Django falló al arrancar. Revisa los mensajes de arriba."
    exit 1
fi

# 5. Crear el archivo de servicio gunicorn.service con el método "módulo" (Bulletproof)
# Este método ejecuta 'python -m gunicorn' en lugar del ejecutable directo,
# lo que evita al 100% errores de shebang y problemas de compatibilidad de archivos de script de Windows.
echo "[5/8] Escribiendo archivo de servicio Systemd de Gunicorn..."
cat << 'EOF' > /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon for Geotlalli
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/geotlalli
ExecStart=/var/www/geotlalli/venv/bin/python -m gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock geoviewer.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Asegurar saltos de línea Unix en el servicio
sed -i 's/\r$//' /etc/systemd/system/gunicorn.service

# 6. Configurar permisos estrictos para el usuario www-data (Nginx)
echo "[6/8] Aplicando permisos y propiedad a la carpeta del proyecto..."
# Forzar a www-data como dueño
chown -R www-data:www-data "$PROJECT_DIR"

# Permisos estándar: 755 para carpetas, 644 para archivos
find "$PROJECT_DIR" -type d -exec chmod 755 {} \;
find "$PROJECT_DIR" -type f -exec chmod 644 {} \;

# Garantizar que el entorno virtual tenga permisos de ejecución correctos
chmod -R 755 "$PROJECT_DIR/venv/bin"
chmod +x "$PROJECT_DIR/venv/bin/"*

# Asegurar que el socket de gunicorn se cree en una ruta accesible
mkdir -p /run
chmod 755 /run

# 7. Recargar systemd y reiniciar servicios
echo "[7/8] Recargando configuración de Systemd..."
systemctl daemon-reload

echo "[7/8] Habilitando y reiniciando el servicio Gunicorn..."
systemctl enable gunicorn
systemctl restart gunicorn

echo "[7/8] Verificando Nginx..."
if [ -f /etc/nginx/sites-enabled/default ]; then
    echo "Eliminando archivo de configuración Nginx por defecto..."
    rm -f /etc/nginx/sites-enabled/default
fi

# Comprobar sintaxis de Nginx y reiniciar
nginx -t
systemctl restart nginx

# 8. Mostrar diagnóstico final
echo "================================================================="
echo "                ¡REPARACIÓN COMPLETADA CON ÉXITO!                "
echo "================================================================="
echo ""
echo "Estado actual del servicio Gunicorn:"
systemctl status gunicorn --no-pager
echo ""
echo "Últimos logs del Journal de Gunicorn:"
journalctl -u gunicorn --no-pager -n 25
