from typing import List
from app.models.job import OfertaLaboral
from app.core.database import db_cliente

def guardar_ofertas_en_db(ofertas: List[OfertaLaboral]) -> dict:
    """
    Recibe una lista de ofertas laborales y las inserta en la base de datos.

    Convierte los modelos Pydantic a diccionarios y realiza una inserción
    en lote (batch insert) en la tabla 'ofertas_laborales' de Supabase.

    **Args**:
        ofertas (List[OfertaLaboral]): Lista de ofertas ya normalizadas.

    **Returns**:
        dict: Un diccionario con el resultado de la operación (éxito y cantidad).
    """

    if not ofertas:
        return {"exito": True, "insertados": 0, "mensaje": "No se recibieron ofertas para guardar."}
    
    datos_a_insertar = []
    for oferta in ofertas:
        datos_a_insertar.append({
            "titulo": oferta.titulo,
            "empresa": oferta.empresa,
            "enlace": oferta.enlace,
            "tecnologias_raw": oferta.tecnologias_raw,
            "tecnologias_normalizadas": oferta.tecnologias_normalizadas,
            "salario": oferta.salario
        })

    try:
        respuesta = db_cliente.table("ofertas_laborales").upsert(
            datos_a_insertar, 
            on_conflict="enlace",
            ignore_duplicates=True
        ).execute()

        cantidad = len(respuesta.data) if respuesta.data else 0

        if cantidad == 0:
            mensaje_final = "No se insertaron nuevas ofertas (posiblemente ya existían en la base de datos)."
        else:
            mensaje_final = f"{cantidad} ofertas insertadas correctamente."

        return {"exito": True, "insertados": cantidad, "mensaje": mensaje_final }
    
    except Exception as e:
        print(f"Error al guardar ofertas en la base de datos: {e}")
        return {"exito": False, "insertados": 0, "mensaje": f"Error al insertar ofertas: {str(e)}"}
