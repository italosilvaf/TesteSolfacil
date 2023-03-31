from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.plant_model import PlantModel
from schemas.plant_schema import PlantSchemaBase, PlantSchema, PlantSchemaUp
from models.partner_model import PartnerModel
from core.deps import get_session, get_current_user
from sqlalchemy.exc import IntegrityError


router = APIRouter()


# POST Plant
# Esse endpoint o parceiro faz o cadastro de usinas, porem o parceiro so consegue cadastrar uma usina se estiver logado.
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PlantSchemaBase)
async def post_plant(plant: PlantSchemaBase, partner_logado: PartnerModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    new_plant = PlantModel(nome=plant.nome, cep=plant.cep, latitude=plant.latitude, longitude=plant.longitude,
                           capacidade_maxima_GW=plant.capacidade_maxima_GW, partner_id=partner_logado.id)

    async with db as session:
        try:
            session.add(new_plant)
            await session.commit()

            return new_plant
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Já existe uma usina com esse CEP cadastrado.')


# GET Plants
# Esse endpoint retorna todos as usinas cadastradas.
@router.get('/', response_model=List[PlantSchemaBase])
async def get_plants(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlantModel)
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


# GET Plant
# Esse endpoint retorna a usina indicado pelo id.
@router.get('/{plant_id}', response_model=PlantSchema, status_code=status.HTTP_200_OK)
async def get_plant(plant_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlantModel).filter(PlantModel.id == plant_id)
        result = await session.execute(query)
        plant: PlantModel = result.scalars().unique().one_or_none()

        if plant:
            return {
                'id': plant.id,
                'nome': plant.nome,
                'cep': plant.cep,
                'latitude': plant.latitude,
                'longitude': plant.longitude,
                'capacidade_maxima_GW': plant.capacidade_maxima_GW,
                'created_at': plant.created_at_formatted,
                'updated_at': plant.updated_at_formatted,
                'partner_id': plant.partner_id
            }
        else:
            raise HTTPException(detail='Usina não encontrada.',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Plant
# Esse endpoint edita o cadastro de uma usina, porem o parceiro pode editar apenas as usinas que ele cadastrou.
@router.put('/{plant_id}', response_model=PlantSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_plant(plant_id: int, plant: PlantSchemaUp, db: AsyncSession = Depends(get_session), partner_logado: PartnerModel = Depends(get_current_user)):
    async with db as session:
        query = select(PlantModel).filter(PlantModel.id == plant_id)
        result = await session.execute(query)
        plant_up: PlantSchemaBase = result.scalars().unique().one_or_none()

        if plant_up:
            if partner_logado.id == plant_up.partner_id:
                if plant.nome:
                    plant_up.nome = plant.nome
                if plant.cep:
                    plant_up.cep = plant.cep
                if plant.latitude:
                    plant_up.latitude = plant.latitude
                if plant.longitude:
                    plant_up.longitude = plant.longitude
                if plant.capacidade_maxima_GW:
                    plant_up.capacidade_maxima_GW = plant.capacidade_maxima_GW
                
                try:
                    await session.commit()
                    return plant_up
                except IntegrityError:
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                        detail='Já existe uma usina com esse CEP cadastrado.')
            else:
                raise HTTPException(
                    detail='O parceiro logado não tem permissão para modificar esta usina.', status_code=status.HTTP_403_FORBIDDEN)
        else:
            raise HTTPException(detail='Usina não encontrada.',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Plant
# Esse endpoint deleta o cadastro de uma usina, porem o parceiro pode deletar apenas as usinas que ele cadastrou.
@router.delete('/{plant_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_plant(plant_id: int, db: AsyncSession = Depends(get_session), partner_logado: PartnerModel = Depends(get_current_user)):
    async with db as session:
        query = select(PlantModel).filter(PlantModel.id == plant_id)
        result = await session.execute(query)
        plant_del: PlantModel = result.scalars().unique().one_or_none()

        if plant_del:
            if partner_logado.id == plant_del.partner_id:
                await session.delete(plant_del)
                await session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)

            else:
                raise HTTPException(
                    detail='O parceiro logado não tem permissão para deletar esta usina.', status_code=status.HTTP_403_FORBIDDEN)
        else:
            raise HTTPException(detail='Usina não encontrada.',
                                status_code=status.HTTP_404_NOT_FOUND)
