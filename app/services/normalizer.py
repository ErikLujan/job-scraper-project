from typing import List

TECNOLOGIAS_VALIDAS = {
    "python", "javascript", "typescript", "java", "c#", "c++", "ruby", "php", 
    "go", "golang", "rust", "swift", "kotlin", "sql", "postgresql", "mysql", 
    "mongodb", "redis", "aws", "azure", "gcp", "docker", "kubernetes", 
    "react", "angular", "vue", "node", "nodejs", "django", "flask", "fastapi",
    "spring", "html", "css", "git", "linux"
}

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
        return None
    
    texto_limpio = nombre_crudo.strip().lower()
    texto_normalizado = MAPEO_TECNOLOGIAS.get(texto_limpio, texto_limpio)

    if texto_normalizado in TECNOLOGIAS_VALIDAS:
        if texto_normalizado == "aws": return "AWS"
        if texto_normalizado == "sql": return "SQL"
        return texto_normalizado.capitalize()
    
    return None

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

    tecnologias_limpias = set()

    for tech in tecnologias_raw:
        tech_valida = normalizar_tecnologia(tech)
        if tech_valida:
            tecnologias_limpias.add(tech_valida)

    return list(tecnologias_limpias)