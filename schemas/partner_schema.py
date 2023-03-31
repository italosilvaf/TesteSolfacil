from typing import Optional, List
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from schemas.plant_schema import PlantSchema
from core.security import valida_cnpj, apenas_numeros


# Schema base do parceiro
class PartnerSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    cnpj: str
    email: EmailStr

    # Validador de CNPJ
    @validator('cnpj')
    def validate_cnpj_partner(cls, cnpj):
        if valida_cnpj(cnpj=cnpj) == False :
            raise ValueError('CNPJ Inválido!')
    
        return cnpj

    class Config:
        orm_mode = True


# Schema do perceiro herdada do base e que tem adicional dos campos de data de criação e de edição do cadastro.
class PartnerSchema(PartnerSchemaBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Schema do perceiro herdada do PartnerSchema e que tem adicional da lista de usinas que tal parceiro cadastrou.
class PartnerSchemaListPlants(PartnerSchema):
    plants: Optional[List[PlantSchema]]


# Schema do perceiro herdada do base e que tem adicional do campo de senha.
class PartnerSchemaCreate(PartnerSchemaBase):
    password: str


# Schema do perceiro herdada do base e que tem adicional do campo de senha, porem todos os campos são opcionais.
class PartnerSchemaUp(PartnerSchemaBase):
    name: Optional[str]
    cnpj: Optional[str]
    email: Optional[str]
    password: Optional[str]
