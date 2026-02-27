from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.core.database import db_cliente
from app.services.normalizer import normalizar_tecnologia

router = APIRouter()

@router.get("/ofertas")
def obtener_ofertas(
    tecnologia: Optional[str] = Query(None, description="Filtrar ofertas por tecnología"),
    pagina: int = Query(1, ge=1, description="Número de página actual"),
    limite: int = Query(20, ge=1, le=100, description="Cantidad de ofertas por pagina (máximo 100)")
) -> dict:
    """
    Obtiene un listado paginado de las ofertas laborales guardadas.
    Permite filtrar opcionalmente por una tecnología específica.

    **Args**:
        tecnologia (str, opcional): El nombre de la tecnología para filtrar las ofertas.
        pagina (int): El número de página a obtener (inicia en 1).
        limite (int): La cantidad de ofertas a mostrar por página (máximo 100).

    **Returns**:
        dict: Un diccionario con la información de paginación y la lista de ofertas laborales.

    **Raises**:
        HTTPException: Si ocurre un error al consultar la base de datos o procesar la solicitud.
    """

    try:
        offset = (pagina - 1) * limite

        query = db_cliente.table("ofertas_laborales").select("*", count="exact")

        if tecnologia:
            tech_limpia = normalizar_tecnologia(tecnologia)
            query = query.contains("tecnologias_normalizadas", [tech_limpia])

        query = query.range(offset, offset + limite - 1).order("id", desc=True)

        respuesta = query.execute()
        datos = respuesta.data

        if not datos:
            if tecnologia:
                return {"mensaje": f"No se encontraron ofertas laborales para la tecnología '{tecnologia}'."}
            else:
                return {"mensaje": "No se encontraron ofertas laborales en esta pagina."}

        total_registros = respuesta.count if respuesta.count is not None else 0
        total_paginas = (total_registros + limite - 1) // limite if total_registros > 0 else 0
        
        return {
            "paginacion": {
                "pagina_actual": pagina,
                "limite": limite,
                "total_registros": total_registros,
                "total_paginas": total_paginas
            },
            "datos": datos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ofertas: {str(e)}")

@router.get("/empresa/{nombre_empresa}")
def obtener_ofertas_por_empresa(nombre_empresa: str) -> dict:
    """
    Obtiene todas las ofertas laborales asociadas a una empresa específica.

    Utiliza una búsqueda flexible (case-insensitive) para encontrar
    coincidencias parciales o totales en el nombre de la empresa.

    **Args**:
        nombre_empresa (str): El nombre de la empresa a buscar.

    **Returns**:
        dict: Un resumen con la cantidad de ofertas y la lista de las mismas.
    """

    try:
        respuesta = db_cliente.table("ofertas_laborales").select("*").ilike("empresa", f"%{nombre_empresa}%").order("creado_en", desc=True).execute()

        datos = respuesta.data

        if not datos:
            return {"mensaje": f"No se encontraron ofertas activas para la empresa '{nombre_empresa}'."}
        
        return {
            "empresa_buscada": nombre_empresa,
            "total_ofertas": len(datos),
            "datos": datos
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ofertas por empresa: {str(e)}")