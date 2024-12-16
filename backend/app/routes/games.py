from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.database import db

router = APIRouter()

# Modelo de entrada
class Game(BaseModel):
    appid: int
    name: str
    tags: Dict[str, int]

@router.post("/", status_code=201)
async def agregar_juego(juego: Game):
    collection = db.get_collection("game_database", "juegos")  # Obtener la colección juegos

    # Verificar si el juego ya existe
    existe = await collection.find_one({"appid": juego.appid})
    if existe:
        return {"mensaje": f"El juego con appid {juego.appid} ya existe."}

    # Guardar el juego en MongoDB
    juego_data = {
        "_id": juego.appid,
        "name": juego.name,
        "tags": juego.tags
    }

    try:
        result = await collection.insert_one(juego_data)
        if result.inserted_id:
            return {"mensaje": "Juego agregado exitosamente", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar el juego: {e}")
