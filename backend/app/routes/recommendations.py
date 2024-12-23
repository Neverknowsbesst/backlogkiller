from fastapi import APIRouter, HTTPException, Depends
from app.services.recommendations import generar_recomendaciones
from app.database import db

router = APIRouter()

@router.get("/{steam_id}")
async def obtener_recomendaciones(steam_id: str):
    # Conectarse a la colección de usuarios
    await db.connect()
    usuarios_collection = db.get_collection("game_database", "usuarios")

    # Buscar el usuario por steam_id
    usuario = await usuarios_collection.find_one({"_id": steam_id})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Generar recomendaciones para el usuario encontrado
    recomendaciones = await generar_recomendaciones(usuario)
    if not recomendaciones:
        raise HTTPException(status_code=404, detail="No se encontraron recomendaciones.")
    
    return recomendaciones
