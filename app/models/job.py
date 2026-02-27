from pydantic import BaseModel, Field
from typing import Optional, List

class OfertaLaboral(BaseModel):
    """
    Modelo de datos que representa una oferta laboral extraída.

    Utiliza Pydantic para validar y esquematizar la información obtenida
    por el scraper antes de procesarla o guardarla en la base de datos.
    """

    titulo: str = Field(..., description="El titulo del puesto")
    empresa: str = Field(..., description="Nombre de la empresa que publica la oferta")
    enlace: str = Field(..., description="URL directa a la publicacion de la oferta laboral")
    tecnologias_raw: List[str] = Field(default_factory=list, description="Lista de tecnologias tal como aparecen en la oferta")
    tecnologias_normalizadas: List[str] = Field(default_factory=list, description="Lista de tecnologias limpias y estandarizadas")
    salario: Optional[str] = Field(None, description="Rango salarial ofrecido, solo si está disponible")