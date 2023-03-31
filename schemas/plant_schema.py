from typing import Optional
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from core.security import verifica_apenas_numeros


# Schema base da usina
class PlantSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    cep: str
    latitude: float
    longitude: float
    capacidade_maxima_GW: int
    partner_id: Optional[int]

    @validator('cep')
    def validate_cep(cls, cep):
        if len(cep) != 8:
            raise ValueError('CEP Inválido, não contem 8 caracteres! ')
        
        if verifica_apenas_numeros(cep) == False:
            raise ValueError('CEP Inválido, não contem apenas números!')

        return cep

    class Config:
        orm_mode = True


# Schema da usina herdada do base e que tem adicional dos campos de data de criação e de edição do cadastro.
class PlantSchema(PlantSchemaBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Schema do perceiro herdada do base, porem todos os campos são opcionais.
class PlantSchemaUp(PlantSchemaBase):
    nome: Optional[str]
    cep: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    capacidade_maxima_GW: Optional[int]
