import os
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.rate_limiter import limiter 
from app.api.health import router as health_router
from app.api.scraper_routes import router as scraper_router
from app.api.analytics_routes import router as analytics_router
from app.api.jobs_routes import router as jobs_router
from app.api.auth_routes import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Job Scraper API",
        description="Motor analítico para extraer y normalizar ofertas laborales.",
        version="1.0.0"
    )

    # --- Rate Limiting ---
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ---  CORS (Cross-Origin Resource Sharing) --- 
    origenes_permitidos = [
        "http://localhost:4200",
        "http://localhost:8000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origenes_permitidos,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # --- Cabeceras de Seguridad (Security Headers) ---
    @app.middleware("http")
    async def agregar_cabeceras_seguridad(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff" # --> # Evita que el navegador intente descifrar el tipo de archivo y ejecute código malicioso
        response.headers["X-Frame-Options"] = "DENY" # --> # Protección contra Clickjacking
        response.headers["X-XSS-Protection"] = "1; mode=block" # --> # Activa el filtro XSS nativo del navegador
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains" # --> # Fuerza conexiones HTTPS estrictas

        return response

    # --- Inclusión de Rutas ---
    app.include_router(health_router, prefix="/api")
    app.include_router(scraper_router, prefix="/api")
    app.include_router(analytics_router, prefix="/api")
    app.include_router(jobs_router, prefix="/api")
    app.include_router(auth_router, prefix="/api", tags=["Autenticación"])

    return app

app = create_app()

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=puerto, 
        reload=False,
        proxy_headers=True, 
        forwarded_allow_ips="*"
    )