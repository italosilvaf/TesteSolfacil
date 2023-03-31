from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.partner_model import PartnerModel
from schemas.partner_schema import PartnerSchema
from core.deps import get_session


router = APIRouter()


# GET Last Partners
# Esse endpoint retorna os 10 últimos parceiros cadastrados.
@router.get('/', response_model=List[PartnerSchema])
async def get_partners(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = query = select(PartnerModel).order_by(
            PartnerModel.created_at.desc()).limit(10)
        result = await session.execute(query)
        partners: List[PartnerSchema] = result.scalars(
        ).unique().all()

        if partners:
            return [{
                'id': partner.id,
                'name': partner.name,
                'cnpj': partner.cnpj,
                'email': partner.email,
                'password': partner.password,
                'created_at': partner.created_at_formatted,
                'updated_at': partner.updated_at_formatted,
            } for partner in partners]
        else:
            raise HTTPException(
                detail='Nenhum parceiro cadastrado.', status_code=status.HTTP_404_NOT_FOUND)
