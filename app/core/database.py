import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Las variables de entorno SUPABASE_URL y SUPABASE_KEY deben estar definidas.")

def obtener_cliente_db() -> Client:
    """
    Inicializa y retorna el cliente de conexión a Supabase.

    Utiliza las credenciales almacenadas en las variables de entorno
    para autenticarse contra el proyecto de Supabase.

    **Returns**:
        Client: La instancia del cliente de Supabase lista para hacer consultas.
    """

    return create_client(SUPABASE_URL, SUPABASE_KEY)

db_cliente = obtener_cliente_db()