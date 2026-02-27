from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.scraper_routes import router as scraper_router
from app.api.analytics_routes import router as analytics_router
from app.api.jobs_routes import router as jobs_router

def create_app() -> FastAPI:
    """
    Inicializa y configura la aplicación principal de FastAPI.

    Registra los routers de los diferentes módulos de la API
    y establece la configuración y metadatos iniciales del servidor.

    **Returns**:
        FastAPI: La instancia configurada de la aplicación FastAPI.
    """

    app = FastAPI(
        title="Job Scraper API",
        description="Motor analitico para extraer y normalizar ofertas laborales.",
        version="1.0.0"
    )

    app.include_router(health_router, prefix="/api")
    app.include_router(scraper_router, prefix="/api")
    app.include_router(analytics_router, prefix="/api")
    app.include_router(jobs_router, prefix="/api")

    return app

app = create_app()