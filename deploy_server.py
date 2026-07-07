"""
Script de despliegue: sube los archivos modificados al servidor vía SFTP usando paramiko.
"""
import paramiko
import os
import sys

HOST = "174.136.38.37"
PORT = 22
USER = "root"
PASSWORD = "6nPH)xdY2[0lB7"
REMOTE_BASE = "/var/www/geotlalli"

LOCAL_BASE = os.path.dirname(os.path.abspath(__file__))
DEPLOY_BASE = os.path.join(LOCAL_BASE, "despliegue_geotlalli")

# Archivos a subir: (ruta local relativa al DEPLOY_BASE, ruta remota relativa al REMOTE_BASE)
FILES = [
    ("mapapp/templates/mapapp/index.html",  "mapapp/templates/mapapp/index.html"),
    ("mapapp/views.py",                     "mapapp/views.py"),
    ("mapapp/urls.py",                      "mapapp/urls.py"),
    ("mapapp/models.py",                    "mapapp/models.py"),
]

def deploy():
    print(f"Conectando a {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=30)
    sftp = client.open_sftp()
    print("✅ Conexión SSH/SFTP establecida.\n")

    for local_rel, remote_rel in FILES:
        local_path = os.path.join(DEPLOY_BASE, local_rel)
        remote_path = f"{REMOTE_BASE}/{remote_rel}"

        if not os.path.exists(local_path):
            print(f"  ⚠️  No encontrado localmente: {local_path}")
            continue

        print(f"  📤 Subiendo: {local_rel}")
        print(f"       → {remote_path}")
        sftp.put(local_path, remote_path)
        print(f"  ✅ Subido correctamente.\n")

    sftp.close()

    # Reiniciar servicios
    print("🔄 Reiniciando Gunicorn y Nginx en el servidor...")
    commands = [
        "chown -R www-data:www-data /var/www/geotlalli",
        "find /var/www/geotlalli -type d -exec chmod 755 {} \\;",
        "find /var/www/geotlalli -type f -exec chmod 644 {} \\;",
        "systemctl restart gunicorn",
        "systemctl restart nginx",
    ]
    for cmd in commands:
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_code = stdout.channel.recv_exit_status()
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        if exit_code == 0:
            print(f"  ✅ OK: {cmd}")
        else:
            print(f"  ⚠️  {cmd}")
            if err:
                print(f"       Error: {err}")

    client.close()
    print("\n🚀 ¡Despliegue completado! El servidor está actualizado.")

if __name__ == "__main__":
    try:
        deploy()
    except Exception as e:
        print(f"\n❌ Error durante el despliegue: {e}")
        sys.exit(1)
