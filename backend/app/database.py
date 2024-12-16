from motor.motor_asyncio import AsyncIOMotorClient
from app.config import config

class Database:
    def __init__(self):
        self.client = None

    async def connect(self):
        if self.client is None:
            try:
                self.client = AsyncIOMotorClient(config.MONGO_URI)
                print("Conexión a MongoDB exitosa")
            except Exception as e:
                print(f"Error al conectar a MongoDB: {e}")
                raise

    async def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
            print("Desconexión de MongoDB exitosa")

    def get_collection(self, db_name: str, collection_name: str):
        if not self.client:
            raise Exception("La conexión a la base de datos no está establecida.")
        return self.client[db_name][collection_name]

# Instancia global de la base de datos
db = Database()
