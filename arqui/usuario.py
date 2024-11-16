import requests
import pymongo
from pymongo import MongoClient

def obtener_datos_juegos(api_key, user_id):
    # URL de la API para obtener los juegos del usuario
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    
    params = {
        'key': api_key,
        'steamid': user_id,
        'include_played_free_games': True,
        'include_appinfo': True,
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()  # Retorna los datos en formato JSON
    else:
        print(f"Error al obtener datos: {response.status_code}")
        return None

def guardar_en_mongodb(data, user_id, db_name="backlogkiller", collection_name="user_games"):
    # Conexión a MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]

    # Procesar y estructurar los datos
    juegos = data.get('response', {}).get('games', [])
    juegos_formateados = [
        {
            "appid": juego["appid"],
            "name": juego.get("name", f"Juego {juego['appid']}"),  # Nombre opcional
            "playtime_forever": juego.get("playtime_forever", 0)
        }
        for juego in juegos
    ]

    # Crear el documento del usuario
    documento_usuario = {
        "_id": user_id,  # ID del usuario como identificador único
        "games": juegos_formateados
    }

    # Guardar o actualizar en la colección
    collection.replace_one({"_id": user_id}, documento_usuario, upsert=True)
    print(f"Datos de los juegos del usuario {user_id} guardados en MongoDB.")

if __name__ == "__main__":
    API_KEY = 'D0772A49646FE9E0401FEE0FABEF7055'  # Reemplaza con tu API Key
    USER_ID = '76561198042982653'  # Reemplaza con el ID del usuario de Steam

    # Obtener datos de juegos
    datos_juegos = obtener_datos_juegos(API_KEY, USER_ID)
    
    if datos_juegos:
        # Guardar datos en MongoDB
        guardar_en_mongodb(datos_juegos, USER_ID)
