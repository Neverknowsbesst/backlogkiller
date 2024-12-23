from fastapi import APIRouter, HTTPException
from app.services.steam_api import guardar_biblioteca_en_mongodb, obtener_biblioteca_steam
from app.database import db

router = APIRouter()

@router.post("/{steam_id}/biblioteca")
async def importar_biblioteca(steam_id: str):

    #Importa la biblioteca de Steam y la guarda en la base de datos.
  
    try:
        # Guardar la biblioteca en MongoDB
        await guardar_biblioteca_en_mongodb(steam_id)
        return {"mensaje": "Biblioteca importada correctamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{steam_id}/biblioteca")
async def obtener_biblioteca(steam_id: str):   
    
    # Obtener la colección de usuarios de la base de datos
    collection = db.get_collection("game_database", "usuarios")

    # Buscar al usuario en la base de datos
    usuario = await collection.find_one({"_id": steam_id})
    
    if usuario:
        return {"biblioteca": usuario.get("biblioteca", [])}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
@router.delete("/{steam_id}/biblioteca/{appid}")
async def eliminar_juego(steam_id: str, appid: int):
    # Conectarse a la base de datos
    usuarios_collection = db.get_collection("game_database", "usuarios")
    
    # elimina juego de la biblioteca del usuario
    result = await usuarios_collection.update_one(
        {"_id": steam_id},
        {"$pull": {"biblioteca": {"appid": appid}}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Juego no encontrado en la biblioteca.")
    
    return {"mensaje": f"Juego {appid} eliminado exitosamente."}
