from typing import Optional
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime


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
    def validate_cep_length(cls, cep):
        if len(cep) != 8:
            raise ValueError('CEP Inválido!')
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
