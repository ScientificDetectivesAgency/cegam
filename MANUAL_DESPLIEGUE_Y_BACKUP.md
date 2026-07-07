# Manual de Copias de Seguridad (Backup) y Despliegue en el Servidor
## Plataforma Visor de Datos Geográficos (Quintana Roo)

Este documento contiene la guía paso a paso para realizar copias de seguridad de la base de datos desde **DBeaver** en formato `.tar`, subir los cambios, restaurar la base de datos en el servidor y actualizar el visor web.

---

## 📋 Resumen de Datos del Servidor

* **Servidor (IP):** `174.136.38.37`
* **Usuario SSH:** `root`
* **Contraseña SSH:** `6nPH)xdY2[0lB7`
* **Ruta del Proyecto:** `/var/www/geotlalli`
* **Base de Datos Destino:** `costas` (PostgreSQL)

---

## 🛠️ PARTE 1: Generación de Copia de Seguridad (.tar) en DBeaver

Para respaldar tu base de datos local en el formato correcto para el servidor (`tar`), sigue estos pasos:

1. **Abrir DBeaver** y conectar con la base de datos local de PostgreSQL.
2. En el panel izquierdo (Navegador de bases de datos), localiza tu base de datos de trabajo.
3. Haz **clic derecho** sobre la base de datos -> selecciona **Herramientas (Tools)** -> **Copia de seguridad (Backup)**.
4. **Selección de Objetos:**
   * En la lista de esquemas, asegúrate de marcar las casillas correspondientes a tus tablas de datos (usualmente `public` o `datos` según tengas estructurado tu PostgreSQL).
   * Haz clic en **Siguiente (Next)**.
5. **Configuración del Formato y Salida (Format & Output):**
   * **Formato (Format):** Selecciona **`TAR`** en la lista desplegable. *Este formato es compatible directamente con `pg_restore`*.
   * **Compresión (Compression):** Déjalo en `Ninguno` (o `default`).
   * **Codificación (Encoding):** `UTF-8`.
   * **Archivo de salida (Output file/folder):** Elige la ruta de tu computadora donde quieres guardarlo y nómbralo como **`costas.tar`**.
6. **Ruta del Cliente PostgreSQL (Client/Binary Path):**
   * DBeaver utiliza la herramienta nativa `pg_dump` de PostgreSQL para generar el backup.
   * Si es la primera vez, DBeaver te pedirá la ruta de los archivos binarios de PostgreSQL local. Apunta a la carpeta `bin` de tu instalación de PostgreSQL (por ejemplo: `C:\Program Files\PostgreSQL\16\bin` o la versión que utilices).
7. Haz clic en **Iniciar (Start)**.
8. Espera que la barra de progreso finalice con éxito. Tu archivo **`costas.tar`** ya está listo en tu carpeta local.

---

## 📂 PARTE 2: Subir el Backup y el Código al Servidor

Puedes transferir el archivo `costas.tar` y los archivos modificados de tu proyecto usando cualquier cliente SFTP/SCP (como **WinSCP** o **FileZilla**), o utilizando Git si mantienes el repositorio sincronizado.

### Opción A: A través de WinSCP / FileZilla
1. Conéctate al servidor mediante SFTP con los datos:
   * **Host:** `174.136.38.37`
   * **Usuario:** `root`
   * **Contraseña:** `6nPH)xdY2[0lB7`
   * **Puerto:** `22`
2. En la ventana izquierda (Local), busca los archivos actualizados y el archivo **`costas.tar`**.
3. En la ventana derecha (Servidor), navega a la ruta: `/var/www/geotlalli`
4. **Sube el archivo `costas.tar`** directamente a la raíz de la carpeta `/var/www/geotlalli`.
5. **Sube los archivos de código modificados** (los archivos dentro de `mapapp/`, etc.).

### Opción B: A través de Git (Recomendado para el código)
Si configuraste Git en local:
```bash
git add .
git commit -m "Actualizacion visor: leyendas, capas y fixes de reset"
git push origin main
```
Y luego en el servidor ejecutas `git pull` para bajar los cambios de código. *Nota: El archivo `.tar` de la base de datos es mejor subirlo por SFTP debido a su tamaño.*

---

## 🔄 PARTE 3: Restaurar la Base de Datos en el Servidor

Una vez que el archivo `costas.tar` está en el servidor, ejecutas la restauración de la base de datos.

1. **Conéctate por SSH al servidor:**
   En Windows (PowerShell/CMD) o Linux, ejecuta:
   ```bash
   ssh root@174.136.38.37
   ```
   *Ingresa la contraseña:* `6nPH)xdY2[0lB7`

2. **Navega a la carpeta del proyecto:**
   ```bash
   cd /var/www/geotlalli
   ```

3. **Ejecuta el Comando de Restauración Nivel Maestro:**
   Este comando limpia las tablas antiguas antes de inyectar las nuevas, asegurando que no queden datos corruptos o duplicados:
   ```bash
   sudo -u postgres pg_restore -d costas --clean --if-exists /var/www/geotlalli/costas.tar
   ```
   * **`-d costas`**: Indica la base de datos destino (`costas`).
   * **`--clean`**: Borra los objetos anteriores de la base de datos antes de recrearlos.
   * **`--if-exists`**: Evita errores molestos de "no existe" al intentar borrar tablas limpias.
   * **`/var/www/geotlalli/costas.tar`**: Ruta del backup que subiste.

---

## 🚀 PARTE 4: Actualización y Reactivación de la Plataforma Web

Con el código nuevo y la base de datos actualizada, ejecuta los comandos de Django y del sistema para que todo funcione de inmediato.

*Mantente dentro de la conexión SSH de tu servidor y sigue estos pasos:*

### 1. Activar el Entorno Virtual de Python
```bash
cd /var/www/geotlalli
source venv/bin/activate
```

### 2. Recolectar Archivos Estáticos (Crucial para CSS/JS)
Dado que editamos los estilos, animaciones y comportamientos en javascript, debemos recolectar los estáticos para que Nginx los sirva actualizados:
```bash
python manage.py collectstatic --noinput
```

### 3. Aplicar Migraciones de Django (Si aplica)
```bash
python manage.py migrate
```

### 4. Forzar Permisos Correctos para Nginx y Gunicorn
Para evitar errores `403 Forbidden` o que las imágenes y archivos no se carguen:
```bash
# Asignar la propiedad a www-data (el usuario del servidor web Nginx)
chown -R www-data:www-data /var/www/geotlalli

# Asegurar permisos correctos en carpetas (755) y archivos (644)
find /var/www/geotlalli -type d -exec chmod 755 {} \;
find /var/www/geotlalli -type f -exec chmod 644 {} \;
```

### 5. Reiniciar los Servicios (Gunicorn y Nginx)
Esto forzará al servidor a descargar la versión de código en caché y servir la nueva versión turbo del visor:
```bash
systemctl restart gunicorn
systemctl restart nginx
```

---

## ⚡ Solución de Problemas Comunes (Cheat Sheet)

* **¿Las fotos se rompieron en el visor?**
  Asegúrate de que la carpeta de fotos está en la ruta doble requerida por el código y con los permisos correctos:
  ```bash
  mkdir -p /var/www/geotlalli/fotos/fotos
  find /var/www/geotlalli/media/ -type f -iname "*.jpg" -exec mv {} /var/www/geotlalli/fotos/fotos/ \;
  chown -R www-data:www-data /var/www/geotlalli/fotos
  systemctl restart gunicorn
  ```

* **¿La página muestra un error 502 Bad Gateway?**
  Esto significa que Gunicorn se detuvo. Revisa sus logs de error con:
  ```bash
  journalctl -u gunicorn --no-pager -n 50
  ```
  Y vuelve a iniciarlo con: `systemctl restart gunicorn`.

* **¿Los cambios de estilos o botones no se ven reflejados?**
  Limpia la caché de tu navegador con `Ctrl + F5` o abre el visor en una ventana de incógnito. También asegúrate de haber corrido `python manage.py collectstatic --noinput`.

---
¡Felicidades! Siguiendo esta guía podrás realizar despliegues limpios, rápidos y seguros de la plataforma sin contratiempos. 🗺️🌐
