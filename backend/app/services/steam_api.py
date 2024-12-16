import requests
from app.database import db
from app.config import config

async def obtener_biblioteca_steam(steam_id: str):
    #aqui obtenemos la lista de juegos del usuario desde la API de steam

    url = f"{config.BASE_URL}/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": config.STEAM_API_KEY,
        "steamid": steam_id,
        "include_appinfo": True
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error al consultar la API de Steam: {response.status_code}")
    return response.json()["response"]["games"]

async def guardar_biblioteca_en_mongodb(steam_id: str):
    #guarda la biblioteca de juegos de un usuario en la base de datos, incluyendo el tiempo de juego

    juegos = await obtener_biblioteca_steam(steam_id)
    if not juegos:
        raise Exception("No se encontraron juegos en la biblioteca.")

    # Obtener la colección de usuarios
    collection = db.get_collection("game_database", "usuarios")

    # Formatear los datos y guardar/actualizar en la base de datos
    biblioteca = [
        {
            "appid": juego["appid"],
            "name": juego.get("name", "Desconocido"),
            "playtime_forever": juego.get("playtime_forever", 0)  # Agregar el tiempo de juego en minutos
        }
        for juego in juegos
    ]
    
    await collection.update_one(
        {"_id": steam_id},
        {"$set": {"biblioteca": biblioteca}},
        upsert=True
    )
