import json
from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Cambia la URL si es necesario
db = client['backlogkiller']  # Selecciona la base de datos
collection = db['game_tags']  # Selecciona la colección

# Cargar el archivo JSON
file_path = 'C:/Users/matia/OneDrive/Escritorio/arqui/tags_juegos.json'  # Cambia el path si es necesario
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insertar los datos en la colección
collection.insert_many(data)

print("Datos importados exitosamente.")
