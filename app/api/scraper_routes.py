from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.scraper.extractor import obtener_html_renderizado
from app.scraper.remoteok import parsear_remoteok
from app.models.job import OfertaLaboral
from app.services.normalizer import procesar_tecnologias
from app.services.repository import guardar_ofertas_en_db

router = APIRouter()

@router.post("/scraping/ejecutar")
def ejecutar_scraper_dinamico(tecnologia: str = Query(..., description="Tecnología a scrapear")) -> dict:
    """
    Scrapea ofertas de RemoteOK para una tecnología específica de forma dinámica.

    **Args**:
        tecnologia (str): La tecnología para la cual se desean obtener ofertas laborales.

    **Returns**:
        dict: Resumen de la operación incluyendo el estado de la base de datos y las ofertas encontradas.
    """

    tech_limpia = tecnologia.strip().lower()    
    url_target = f"https://remoteok.com/remote-{tech_limpia}-jobs"

    try:
        html_crudo = obtener_html_renderizado(url_target)
        ofertas = parsear_remoteok(html_crudo)

        if not ofertas:
            return {
                "estado": "completado",
                "mensaje": f"No se encontraron ofertas para la tecnología '{tech_limpia}' en este momento"
            }
        
        for oferta in ofertas:
            oferta.tecnologias_normalizadas = procesar_tecnologias(oferta.tecnologias_raw)

        resultado_db = guardar_ofertas_en_db(ofertas)

        respuesta = {
            "estado": "completado",
            "tecnologia_buscada": tech_limpia,
            "ofertas_encontradas": len(ofertas),
            "base_de_datos": resultado_db
        }

        if resultado_db.get("insertados", 0) > 0:
            respuesta["datos"] = ofertas

        return respuesta
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ofertas de RemoteOK para '{tech_limpia}': {str(e)}")