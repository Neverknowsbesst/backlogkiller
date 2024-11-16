import subprocess
import sys
import os

# Parámetros de configuración
mongo_uri = "mongodb://usuario:contraseña@localhost:27017"  # Cambia con tus credenciales y host
db_name = "backlogkiller"  # Nombre de la base de datos
output_directory = "/ruta/del/dump"  # Directorio local para almacenar el dump

def export_database():
    """Exporta la base de datos usando mongodump."""
    try:
        # Verifica si el directorio de salida existe, si no, lo crea
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        # Ejecuta el comando mongodump
        subprocess.run(
            ["mongodump", "--uri", mongo_uri, "--db", db_name, "--out", output_directory],
            check=True
        )
        print(f"Base de datos '{db_name}' exportada exitosamente a {output_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error al exportar la base de datos: {e}")
        sys.exit(1)

def main():
    """Función principal que coordina la exportación de la base de datos."""
    export_database()

if __name__ == "__main__":
    main()
