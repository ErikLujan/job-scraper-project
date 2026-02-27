from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check() -> dict:
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