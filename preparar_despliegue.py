import os
import shutil
import stat

def remove_readonly(func, path, excinfo):
    # En caso de archivos de solo lectura (como caches de python), forzar permisos de escritura y reintentar borrado
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"No se pudo eliminar {path}: {e}")

def main():
    src_dir = r"C:\Users\eurekastein\OneDrive\Documentos\01_PROYECTOS_ACTUALES\GEOEMPRENDIMIENTO"
    dest_dir = os.path.join(src_dir, "despliegue_geotlalli")
    
    # 1. Crear carpeta limpia
    if os.path.exists(dest_dir):
        print(f"Limpiando carpeta de despliegue anterior en: {dest_dir}")
        shutil.rmtree(dest_dir, onerror=remove_readonly)
    os.makedirs(dest_dir, exist_ok=True)
    
    # 2. Definir qué archivos y carpetas copiar
    items_to_copy = [
        "geoviewer",
        "mapapp",
        "static",
        "manage.py",
        "requirements.txt",
        "repara_servidor.sh"
    ]
    
    print("Copiando archivos esenciales para el sitio web...")
    for item in items_to_copy:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                print(f" -> Copiando carpeta: {item}")
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                print(f" -> Copiando archivo: {item}")
                shutil.copy(src_path, dest_path)
        else:
            print(f"⚠️ ADVERTENCIA: No se encontró {item}")

    print("\n=======================================================")
    print("¡Listo! Carpeta 'despliegue_geotlalli' creada con éxito.")
    print("Solo contiene los archivos web necesarios (menos de 5 MB).")
    print("=======================================================")

if __name__ == '__main__':
    main()
