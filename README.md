# Backlogkiller

Backlogkiller es una aplicación que permite gestionar tu biblioteca de juegos en Steam y obtener recomendaciones personalizadas basadas en el tiempo jugado y los tags de tus juegos.

## Instalación

1. Clona este repositorio en tu máquina local:
    ```bash
    git clone https://github.com/neverknowsbesst/backlogkiller.git
    ```

2. Navega a la carpeta del proyecto:
    ```bash
    cd backlogkiller
    ```

3. Crea un entorno virtual (si no tienes uno ya creado):
    ```bash
    python -m venv venv
    ```

4. Activa el entorno virtual:
    - En Windows:
      ```bash
      .\env\Scripts\activate
      ```
    - En macOS/Linux:
      ```bash
      source env/bin/activate
      ```

5. Instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

6. Configura tu clave de API de Steam. Puedes obtenerla desde el sitio web oficial de Steam y almacenarla en tu archivo de configuración.

## Ejecución

Para ejecutar el servidor de desarrollo, usa el siguiente comando:

```bash
uvicorn app.main:app --reload
