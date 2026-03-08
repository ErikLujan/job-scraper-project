from fastapi import APIRouter, Request
from app.core.rate_limiter import limiter

router = APIRouter()

@router.get("/health")
@limiter.limit("10/minute")
def health_check(request: Request) -> dict:
    """
    Verifica el estado de la API.

    Este endpoint es útil para comprobar que el servidor está levantado
    y respondiendo correctamente antes de realizar consultas complejas.

    **Returns**:
        dict: Un diccionario con el estado actual de la API y un mensaje de bienvenida.
    """

    return {
        "status": "ok",
        "message": "El motor del scrapper analitico esta en funcionamiento."
    }