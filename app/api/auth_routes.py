import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import crear_token_acceso
from app.core.rate_limiter import limiter
from fastapi import Request

router = APIRouter()

@router.post("/auth/login")
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Autentica al administrador y genera un token JWT para acceder a rutas protegidas.

    Este endpoint está protegido con un límite de peticiones (Rate Limiting) de 
    5 intentos por minuto para prevenir ataques de fuerza bruta.

    **Args:**
    - request (Request): El objeto de petición de FastAPI (requerido por `slowapi` para rastrear la IP del cliente).
    - form_data (OAuth2PasswordRequestForm): Formulario inyectado automáticamente por FastAPI que contiene las credenciales (`username` y `password`) enviadas por el usuario.

    **Returns:**
    - dict: Un diccionario que cumple con el estándar de respuesta OAuth2:
        - `access_token` (str): El token JWT generado y firmado.
        - `token_type` (str): El esquema de autenticación a utilizar (siempre "bearer").

    **Raises:**
    - HTTPException (401): Si el usuario o la contraseña no coinciden con las credenciales de administrador configuradas en el entorno.
    """
    user_env = os.environ.get("ADMIN_USER")
    pass_env = os.environ.get("ADMIN_PASS")

    if form_data.username != user_env or form_data.password != pass_env:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = crear_token_acceso(data={"sub": form_data.username})
    
    return {"access_token": token, "token_type": "bearer"}