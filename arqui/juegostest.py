import requests
import json
import time

def obtener_tags_juegos():
    # Leer los IDs de los juegos desde el archivo
    with open('ids_juegos.txt', 'r', encoding='utf-8') as archivo:
        ids_juegos = archivo.read().splitlines()  # Leer cada línea como un ID

    juegos = []  # Lista para almacenar la información de cada juego como un objeto JSON
    max_juegos = 100  # Número máximo de juegos a procesar

    for appid in ids_juegos[:max_juegos]:  # Solo procesar los primeros 10 IDs
        # Hacer la solicitud a la API para cada juego
        url = f'https://steamspy.com/api.php?request=appdetails&appid={appid}'
        respuesta = requests.get(url)

        # Comprobar si la respuesta es exitosa
        if respuesta.status_code == 200:
            juego_info = respuesta.json()

            # Verificar si 'tags' y 'name' están disponibles
            if 'tags' in juego_info and 'name' in juego_info:
                juego_data = {
                    "appid": int(appid),  # Convertir a int para MongoDB
                    "name": juego_info['name'],
                    "tags": juego_info['tags']
                }
                juegos.append(juego_data)  # Agregar cada juego como un objeto en la lista
                print(f"Tags para el juego {juego_info['name']} (ID: {appid}): {juego_info['tags']}")
            else:
                print(f"No se encontraron tags o nombre para el juego {appid}.")

        else:
            print(f'Error al obtener datos para el juego {appid}: {respuesta.status_code}')
        
        # Esperar 1 segundo para cumplir con la tasa de solicitud permitida
        time.sleep(1)

    # Guardar todos los juegos en un archivo JSON, en formato de lista
    with open('tags_juegos.json', 'w', encoding='utf-8') as archivo:
        json.dump(juegos, archivo, ensure_ascii=False, indent=4)
    print(f"Tags y nombres de los juegos guardados en 'tags_juegos.json'.")

# Llamar a la función para obtener y guardar los tags de los juegos
obtener_tags_juegos()

