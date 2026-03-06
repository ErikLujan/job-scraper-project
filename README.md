# Job Scraper API

API REST y motor de scraping para la extracción, normalización y análisis de ofertas laborales remotas. El proyecto automatiza la recopilación de datos desde portales de empleo, limpia y unifica la información tecnológica requerida por las empresas, la persiste en base de datos y la expone mediante endpoints con paginación y estadísticas en tiempo real.

## Stack

- **FastAPI** — framework web
- **PostgreSQL (Supabase)** — base de datos relacional hosteada
- **BeautifulSoup4 / Requests** — scraping y parsing HTML
- **uv** — gestión de dependencias y entorno virtual

## Características principales

**Scraping bajo demanda** — el motor de extracción se dispara por endpoint, recibiendo la tecnología objetivo como parámetro.

**Normalización de tecnologías** — algoritmo de limpieza que unifica variaciones de nombres (`React.js`, `ReactJS`, `react` → `React`) para mantener la integridad estadística de los datos.

**Upsert en lote** — las inserciones validan restricciones únicas antes de persistir, evitando duplicados en ofertas ya almacenadas.

**Filtrado y paginación** — los endpoints de listado soportan consultas dinámicas con `ilike` y `contains`, más paginación nativa.

**Módulo de analíticas** — rankings en tiempo real de tecnologías más demandadas y empresas con mayor volumen de publicaciones.

## Endpoints

### POST /api/scraping/ejecutar
Dispara el motor de extracción para una tecnología específica.

<img width="1897" height="744" alt="image" src="https://github.com/user-attachments/assets/55b6e2b3-549d-451a-9380-c0a515d71363" />

### GET /api/ofertas/
Devuelve el listado completo de ofertas guardadas. Soporta los parámetros `pagina`, `limite` y `tecnologia`.

<img width="1889" height="877" alt="image" src="https://github.com/user-attachments/assets/b23dddee-76aa-48ae-9343-34230535af8d" />

### GET /api/empresa/{nombre_empresa}
Busca ofertas filtrando por coincidencias en el nombre de la empresa.

<img width="1891" height="643" alt="image" src="https://github.com/user-attachments/assets/99777b29-7e8e-473a-b0f0-301bec0b3a9e" />

### GET /api/estadisticas/top-tecnologias
Ranking de las tecnologías más repetidas en la base de datos.

<img width="1887" height="647" alt="image" src="https://github.com/user-attachments/assets/89dd6abc-5b6c-474e-bd21-edda1c6ba175" />

### GET /api/estadisticas/top-empresas
Empresas con mayor cantidad de publicaciones activas.

<img width="1893" height="600" alt="image" src="https://github.com/user-attachments/assets/2f060ed9-6783-424f-b2b2-39d4727acdd8" />

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/job-scraper-project.git
cd job-scraper-project

# Crear y activar el entorno virtual
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
uv pip install -r requirements.txt
```

### Variables de entorno

Creá un archivo `.env` en la raíz del proyecto con tus credenciales de Supabase:

```env
SUPABASE_URL=url_supabase
SUPABASE_KEY=anon_key
```

### Levantar el servidor

```bash
uvicorn main:app --reload
```

La documentación interactiva queda disponible en `http://localhost:8000/docs`.
