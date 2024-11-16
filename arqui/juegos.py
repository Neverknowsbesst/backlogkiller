import requests

def obtener_ids_juegos():
    page = 0
    ids_juegos = []  # Lista para almacenar los IDs de los juegos

    # Hacer la solicitud a la API para la página 0
    url = f'https://steamspy.com/api.php?request=all&page={page}'
    respuesta = requests.get(url)
    
    # Comprobar si la respuesta es exitosa
    if respuesta.status_code == 200:
        try:
            datos = respuesta.json()
            print(f"Datos recibidos: {datos}")  # Imprimir los datos recibidos
            
            # Verifica si hay datos devueltos
            if not datos:
                print("No se encontraron datos en la respuesta.")
                return
            
            # Extraer los IDs de los juegos
            for appid, juego in datos.items():
                ids_juegos.append(appid)  # Agregar el ID a la lista

            # Guardar los IDs en un archivo de texto
            with open('ids_juegos.txt', 'w', encoding='utf-8') as archivo:
                for id_juego in ids_juegos:
                    archivo.write(f"{id_juego}\n")  # Escribir cada ID en una nueva línea
            
            print(f"Se han guardado {len(ids_juegos)} IDs de juegos en 'ids_juegos.txt'.")
        
        except ValueError as e:
            print(f"Error al procesar los datos JSON: {e}")
    else:
        print(f'Error al obtener datos: {respuesta.status_code}')
        print(f'Respuesta: {respuesta.text}')  # Imprimir el contenido de la respuesta

# Llamar a la función para obtener los IDs de los juegos
obtener_ids_juegos()
