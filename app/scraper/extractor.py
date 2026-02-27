from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def obtener_html_renderizado(url: str) -> str:
    """
    Navega a una URL específica y extrae su HTML renderizado.

    Utiliza Playwright para abrir un navegador Chromium en modo headless, espera a que la red esté inactiva (asegurando que el contenido dinámico con JavaScript se haya cargado) y retorna el código fuente de la página.

    **Args**:
        url (str): La dirección web del portal de empleos a scrapear.

    **Returns**:
        str: El contenido HTML completo y renderizado de la página.

    **Raises**:
        Exception: Si ocurre un error al intentar acceder a la página o
                si el tiempo de espera (timeout) se agota.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url)

            page.wait_for_load_state('networkidle')

            html_content = page.content()

            return html_content

        except Exception as e:
            print(f"Error al scrapear {url}: {e}")
            raise e
        
        finally:
            browser.close()