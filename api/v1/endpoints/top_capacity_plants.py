from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.plant_model import PlantModel
from schemas.plant_schema import PlantSchemaBase
from core.deps import get_session


router = APIRouter()


# GET TOP Capacity Plants
# Esse endpoint retorna as 5 usinas de maior capacidade.
@router.get('/', response_model=List[PlantSchemaBase])
async def get_plants(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = query = select(PlantModel).order_by(
            PlantModel.capacidade_maxima_GW.desc()).limit(5)
        result = await session.execute(query)
        plants: List[PlantModel] = result.scalars().unique().all()

        if plants:
            return [{
                'id': plant.id,
                'nome': plant.nome,
                'cep': plant.cep,
                'latitude': plant.latitude,
                'longitude': plant.longitude,
                'capacidade_maxima_GW': plant.capacidade_maxima_GW,
                'partner_id': plant.partner_id
            } for plant in plants]
        else:
            raise HTTPException(detail='Nenhuma usina cadastrada.',
                                status_code=status.HTTP_404_NOT_FOUND)
