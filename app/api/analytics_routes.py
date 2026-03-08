from fastapi import APIRouter, HTTPException, Request
from collections import Counter

from app.core.rate_limiter import limiter
from app.core.database import db_cliente

router = APIRouter()

@router.get("/estadisticas/top-tecnologias")
@limiter.limit("25/minute")
def obtener_top_tecnologias(request: Request, limite: int = 10) -> dict:
    """
    Calcula las tecnologías más demandadas basándose en las ofertas guardadas.

    Consulta la base de datos de Supabase, extrae las listas de tecnologías
    normalizadas de cada oferta y genera un ranking de frecuencias.

    **Args**:
        limite (int, optional): La cantidad de tecnologías a incluir en el ranking. 
                                Por defecto es 10.

    **Returns**:
        dict: Un diccionario con el total de ofertas analizadas y el ranking.
    """

    try:
        respuesta = db_cliente.table("ofertas_laborales").select("tecnologias_normalizadas").execute()

        ofertas = respuesta.data
        if not ofertas:
            return {"mensaje": "No se encontraron ofertas laborales en la base de datos."}
        
        contador = Counter()

        for oferta in ofertas:
            tecnologias = oferta.get("tecnologias_normalizadas", [])
            if tecnologias:
                contador.update(tecnologias)

        top_tech = contador.most_common(limite)

        resultado = [{"tecnologia": tech, "menciones": cuenta } for tech, cuenta in top_tech]

        return {
            "total_ofertas_analizadas": len(ofertas),
            "ranking": resultado
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")
    
@router.get("/estadisticas/top-empresas")
@limiter.limit("25/minute")
def obtener_top_empresas(request: Request, limite: int = 10) -> dict:
    """
    Calcula cuáles son las empresas con más ofertas publicadas en la base de datos.

    **Args**:
        limite (int, optional): Cantidad de empresas a mostrar en el ranking.

    **Returns**:
        dict: Un ranking ordenado de las empresas más activas.
    """

    try:
        respuesta = db_cliente.table("ofertas_laborales").select("empresa").execute()

        ofertas = respuesta.data
        if not ofertas:
            return {"mensaje": "No se encontraron ofertas laborales en la base de datos."}
        
        nombres_empresas = [oferta.get("empresa") for oferta in ofertas if oferta.get("empresa")]

        contador = Counter(nombres_empresas)
        top_empresas = contador.most_common(limite)

        resultado = [{"empresa": nombre, "ofertas_activas": cuenta } for nombre, cuenta in top_empresas]

        return {
            "total_ofertas_analizadas": len(ofertas),
            "ranking": resultado
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")