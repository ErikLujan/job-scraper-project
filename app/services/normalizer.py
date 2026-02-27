from typing import List

MAPEO_TECNOLOGIAS = {
    "py": "Python",
    "python 3": "Python",
    "python3": "Python",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "react.js": "React",
    "reactjs": "React",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "aws": "AWS",
    "amazon web services": "AWS",
    "vue.js": "Vue",
    "vuejs": "Vue",
    "go": "Golang",
}

def normalizar_tecnologia(nombre_crudo: str) -> str:
    """
    Limpia y estandariza el nombre de una tecnología individual.

    Convierte el texto a minúsculas, elimina espacios extra y lo busca
    en el diccionario de mapeo. Si no existe un alias, devuelve el
    texto original capitalizado.

    **Args**:
        nombre_crudo (str): La etiqueta extraída directamente del portal.

    **Returns**:
        str: El nombre oficial de la tecnología.
    """

    if not nombre_crudo:
        return ""
    
    texto_limpio = nombre_crudo.strip().lower()

    return MAPEO_TECNOLOGIAS.get(texto_limpio, texto_limpio.capitalize())

def procesar_tecnologias(tecnologias_raw: List[str]) -> List[str]:
    """
    Procesa una lista completa de tecnologías crudas.

    Aplica la normalización a cada elemento y elimina duplicados
    (por ejemplo, si un anuncio decía "Python" y "Py" al mismo tiempo).

    **Args**:
        tecnologias_raw (List[str]): Lista de etiquetas originales.

    **Returns**:
        List[str]: Lista de etiquetas estandarizadas y sin repetir.
    """

    tecnologias_limpias = set() # -> Usmos el set para evitar la duplicación

    for tech in tecnologias_raw:
        tech_normalizada = normalizar_tecnologia(tech)
        if tech_normalizada:
            tecnologias_limpias.add(tech_normalizada)

    return list(tecnologias_limpias)