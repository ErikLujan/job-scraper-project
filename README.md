# Job Scraper API

Motor analítico y API REST desarrollada para la extracción, normalización y análisis de ofertas laborales remotas en tiempo real. 

Este proyecto automatiza la recopilación de datos desde portales de empleo, limpia la información tecnológica requerida por las empresas y la persiste en una base de datos relacional, exponiendo endpoints para el consumo paginado y el análisis estadístico del mercado.

## Arquitectura y Tecnologías

* **Lenguaje:** Python
* **Framework Web:** FastAPI
* **Base de Datos:** PostgreSQL (vía Supabase)
* **Gestor de Paquetes:** uv
* **Scraping:** BeautifulSoup4 / Requests

## Características Principales

* **Scraping Dinámico:** Extracción de ofertas bajo demanda basada en parámetros de tecnología.
* **Normalización de Datos:** Algoritmo de limpieza que unifica las variaciones de nombres de tecnologías (ej. "React.js", "ReactJS", "react" -> "React") para mantener la integridad estadística.
* **Persistencia Inteligente (Upsert):** Inserciones en lote (batch inserts) con validación de restricciones únicas (`UNIQUE constraint`) para evitar la duplicación de ofertas preexistentes en la base de datos.
* **Consumo Optimizado:** Endpoints de listado con paginación nativa y filtrado mediante consultas SQL dinámicas (`ilike`, `contains`).
* **Módulo de Analíticas:** Generación de rankings en tiempo real de las tecnologías más demandadas y las empresas con mayor volumen de contratación.

## Endpoints Principales

* ### POST /api/scraping/ejecutar:
  * Dispara el motor de extracción para una tecnología específica.
 
  <img width="1897" height="744" alt="image" src="https://github.com/user-attachments/assets/55b6e2b3-549d-451a-9380-c0a515d71363" />


* ### GET /api/ofertas/:
  * Devuelve el listado completo de ofertas guardadas (soporta parámetros pagina, limite y tecnologia).
 
  <img width="1889" height="877" alt="image" src="https://github.com/user-attachments/assets/b23dddee-76aa-48ae-9343-34230535af8d" />

* ### GET /api/empresa/{nombre_empresa}:
  * Busca ofertas activas filtrando por coincidencias en el nombre de la compañía.
 
  <img width="1891" height="643" alt="image" src="https://github.com/user-attachments/assets/99777b29-7e8e-473a-b0f0-301bec0b3a9e" />

* ### GET /api/estadisticas/top-tecnologias:
  * Retorna un ranking de las habilidades más repetidas en la base de datos.

  <img width="1887" height="647" alt="image" src="https://github.com/user-attachments/assets/89dd6abc-5b6c-474e-bd21-edda1c6ba175" />

 
* ### GET /api/estadisticas/top-empresas:
  * Retorna las compañías con mayor cantidad de publicaciones.
 
  <img width="1893" height="600" alt="image" src="https://github.com/user-attachments/assets/2f060ed9-6783-424f-b2b2-39d4727acdd8" />

## Instalación y Uso Local

1. Clonar el repositorio:
    ```bash
    git clone [https://github.com/TU_USUARIO/job-scraper-project.git](https://github.com/TU_USUARIO/job-scraper-project.git)
    cd job-scraper-project
    ```

2. Crear y activar el entorno virtual usando uv:
    ```
    uv venv
    # En Windows:
    .venv\Scripts\activate
    ```

3. Instalar las dependencias:
    ```
    uv pip install -r requirements.txt
    ```

4. Configurar las variables de entorno. Crear un archivo .env en la raíz con tus credenciales de Supabase:
    ```
    SUPABASE_URL="url_supabase"
    SUPABASE_KEY="anon_key"
    ```
   
5. Ejecutar el servidor de desarrollo:
    ```
    uvicorn main:app --reload
    ```
6. Acceder a la documentación interactiva en: http://localhost:8000/docs
