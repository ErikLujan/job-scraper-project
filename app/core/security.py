import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

ALGORITHM = "HS256"
TIEMPO_EXPIRACION_MINUTOS = 30

def crear_token_acceso(data: dict) -> str:
    """
    Genera un token JWT (JSON Web Token) firmado con una fecha de expiración.

    **Args:**
    - data (dict): Diccionario con la información a encriptar en el payload del token (típicamente el usuario bajo la clave `sub`).

    **Returns:**
    - str: El token JWT generado, firmado y codificado en formato de cadena de texto.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TIEMPO_EXPIRACION_MINUTOS)
    to_encode.update({"exp": expire})
    
    clave_secreta = os.environ.get("JWT_SECRET", "clave_por_defecto_insegura")
    encoded_jwt = jwt.encode(to_encode, clave_secreta, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Desencripta el token JWT recibido en las cabeceras y verifica su validez.
    
    Este método actúa como dependencia de seguridad, asegurándose de que el token 
    no haya expirado y que la firma sea legítima antes de dejar pasar la petición.

    **Args:**
    - token (str): El token JWT extraído automáticamente por FastAPI desde el header `Authorization: Bearer <token>`.

    **Returns:**
    - str: El nombre de usuario (`username`) extraído del payload si la validación es exitosa.

    **Raises:**
    - HTTPException (401): Si el payload no contiene un usuario válido.
    - HTTPException (401): Si el tiempo de expiración del token (`exp`) ya pasó.
    - HTTPException (401): Si el token está malformado o la firma no coincide con el servidor.
    """
    clave_secreta = os.environ.get("JWT_SECRET", "clave_por_defecto_insegura")
    
    try:
        payload = jwt.decode(token, clave_secreta, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return username
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="El token expiró. Por favor, iniciá sesión de nuevo."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales inválidas."
        )