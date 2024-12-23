from app.database import db

async def generar_recomendaciones(usuario, limite_tiempo_jugado=300, limite_tiempo_minimo=30): #aqui se establecen los parametros de tiempo para recomendar
    # Conectarse a la base de datos
    await db.connect()
    
    # Obtener las colecciones necesarias
    juegos_collection = db.get_collection("game_database", "juegos")
    
    # Obtener los juegos en la base de datos
    juegos_en_bd = await juegos_collection.find().to_list(1000)
    juegos_en_bd_ids = {juego["_id"] for juego in juegos_en_bd}
    
    # Filtrar los juegos del usuario que esten en la base de datos
    juegos_usuario = [
        juego for juego in usuario["biblioteca"]
        if juego["appid"] in juegos_en_bd_ids
    ]
    
    # Filtrar juegos con mas de 5 horas jugadas
    juegos_usuario_mas_tiempo = [
        juego for juego in juegos_usuario
        if juego["playtime_forever"] >= limite_tiempo_jugado
    ]
    
    # Filtrar juegos con menos de 30 minutos jugados
    juegos_usuario_menos_tiempo = [
        juego for juego in juegos_usuario
        if juego["playtime_forever"] < limite_tiempo_minimo
    ]
    
    if not juegos_usuario_mas_tiempo:
        return []

    # Calcular relevancia para juegos con menos tiempo jugado
    recomendaciones = []
    for juego_usuario in juegos_usuario_menos_tiempo:
        relevancia = 0
        juego_bd = next(
            (juego for juego in juegos_en_bd if juego["_id"] == juego_usuario["appid"]),
            None
        )
        if juego_bd:
            tags_juego = set(juego_bd.get("tags", []))
            relevancia = sum(
                len(tags_juego & set(juego_bd_comp.get("tags", [])))
                for juego_bd_comp in juegos_en_bd
                if juego_bd_comp["_id"] in {juego["appid"] for juego in juegos_usuario_mas_tiempo}
            )
            recomendaciones.append({
                "nombre": juego_bd.get("name", f"Juego sin nombre (appid: {juego_usuario['appid']})"),
                "relevancia": relevancia
            })
    
    # Ordenar recomendaciones por relevancia
    recomendaciones.sort(key=lambda x: x["relevancia"], reverse=True)
    return recomendaciones
