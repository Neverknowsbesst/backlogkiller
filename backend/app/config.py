from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    STEAM_API_KEY: str = "D0772A49646FE9E0401FEE0FABEF7055"
    BASE_URL: str = "https://api.steampowered.com"

config = Config()
