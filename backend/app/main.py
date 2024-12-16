from fastapi import FastAPI
from app.routes import users, recommendations, games
from app.database import db  # Instancia global de la base de datos
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conectar a la base de datos al iniciar la aplicación
    try:
        await db.connect()
        print("Base de datos conectada al iniciar la aplicación.")
        yield  # Permitir que el servidor maneje solicitudes
    finally:
        # Desconectar de la base de datos al cerrar la aplicación
        await db.disconnect()
        print("Base de datos desconectada al cerrar la aplicación.")

# Crear la aplicación FastAPI usando el manejador de duración (lifespan)
app = FastAPI(lifespan=lifespan)

# Registrar rutas
app.include_router(users.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(recommendations.router, prefix="/recomendaciones", tags=["Recomendaciones"])
app.include_router(games.router, prefix="/juegos", tags=["Juegos"])

# Configurar las plantillas Jinja2
templates = Jinja2Templates(directory="app/templates")

# Configurar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Ruta para mostrar el formulario o la página de inicio
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
