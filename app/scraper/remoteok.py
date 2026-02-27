from bs4 import BeautifulSoup
from typing import List
from app.models.job import OfertaLaboral

def parsear_remoteok(html: str) -> List[OfertaLaboral]:
    """
    Analiza el HTML de RemoteOK y extrae una lista de ofertas laborales.

    Busca los elementos del DOM específicos del portal (filas con clase 'job'),
    extrae título, empresa, enlace y etiquetas de tecnologías, y retorna
    una lista de objetos validados por Pydantic.

    **Args**:
        html (str): El código fuente completo de la página de RemoteOK.

    **Returns**:
        List[OfertaLaboral]: Una lista de objetos con los datos extraídos y estructurados.
    """

    soup = BeautifulSoup(html, 'html.parser')
    ofertas = []

    filas_trabajo = soup.find_all("tr", class_="job")

    for fila in filas_trabajo:
        try:
            # Extraemos el título
            elemento_titulo = fila.find("h2", itemprop="title")
            titulo = elemento_titulo.text.strip() if elemento_titulo else "Título no disponible"

            # Extraemos la empresa
            elemento_empresa = fila.find("h3", itemprop="name")
            empresa = elemento_empresa.text.strip() if elemento_empresa else "Empresa desconocida"

            # Extraemos el enlace
            enlace_relativo = fila.get("data-url")
            enlace = f"https://remoteok.io{enlace_relativo}" if enlace_relativo else "https://remoteok.com"

            #Extraemos el salario
            salario_extraido = None
            elementos_location = fila.find_all("div", class_="location")

            for div in elementos_location:
                texto = div.text.strip()

                if "$" in texto or "€" in texto or "£" in texto or "¥" in texto:
                    salario_extraido = texto
                    break

            tecnologias = []
            contenedor_tags = fila.find("td", class_="tags")

            if contenedor_tags:
                tags = contenedor_tags.find_all("h3")
                for tag in tags:
                    texto_tag = tag.text.strip()
                    if texto_tag:
                        tecnologias.append(texto_tag)

            if titulo != "Titulo no disponible":
                oferta = OfertaLaboral(
                    titulo=titulo,
                    empresa=empresa,
                    enlace=enlace,
                    tecnologias_raw=tecnologias,
                    tencologias_normalizadas=[],
                    salario=salario_extraido
                )
                ofertas.append(oferta)

        except Exception as e:
            print(f"Error al procesar una fila especifica: {e}")
            continue

    return ofertas