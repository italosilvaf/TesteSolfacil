from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.partner_model import PartnerModel
from schemas.partner_schema import PartnerSchemaBase, PartnerSchemaCreate, PartnerSchemaUp, PartnerSchema, PartnerSchemaListPlants
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse


router = APIRouter()


# GET Logado
# Esse endpoint retorna o parceiro que está logado.
@router.get('/logado', response_model=PartnerSchemaBase)
def get_logado(partner_logado: PartnerModel = Depends(get_current_user)):
    return partner_logado


# POST Partner / Signup
# Esse endpoint faz o cadastro de parceiros.
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=PartnerSchemaBase)
async def post_partner(partner: PartnerSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_partner: PartnerModel = PartnerModel(
        name=partner.name, cnpj=partner.cnpj, email=partner.email, password=gerar_hash_senha(partner.password))

    async with db as session:
        try:
            session.add(new_partner)
            await session.commit()

            return new_partner
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Já existe um parceiro com esse e-mail ou CNPJ cadastrado.")


# GET Partners
# Esse endpoint retorna todos os parceiros.
@router.get('/', response_model=List[PartnerSchema])
async def get_partners(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PartnerModel)
        result = await session.execute(query)
        partners: List[PartnerSchema] = result.scalars().unique().all()

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


# GET Partner
# Esse endpoint retorna o parceiro indicado pelo id com todas as usinas que o mesmo cadastrou.
@router.get('/{partner_id}', response_model=PartnerSchemaListPlants, status_code=status.HTTP_200_OK)
async def get_partner(partner_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PartnerModel).filter(PartnerModel.id == partner_id)
        result = await session.execute(query)
        partner: PartnerSchemaListPlants = result.scalars().unique().one_or_none()

        if partner:
            return {
                'id': partner.id,
                'name': partner.name,
                'cnpj': partner.cnpj,
                'email': partner.email,
                'password': partner.password,
                'created_at': partner.created_at_formatted,
                'updated_at': partner.updated_at_formatted,
                'plants': partner.plants
            }
        else:
            raise HTTPException(detail='Parceiro não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT Partner
# Esse endpoint edita o cadastro de um parceiro, porem o parceiro pode editar apenas o seu cadastro.
@router.put('/{partner_id}', response_model=PartnerSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_partner(partner_id: int, partner: PartnerSchemaUp, db: AsyncSession = Depends(get_session), partner_logado: PartnerModel = Depends(get_current_user)):
    async with db as session:
        query = select(PartnerModel).filter(PartnerModel.id == partner_id)
        result = await session.execute(query)
        partner_up: PartnerSchemaBase = result.scalars(
        ).unique().one_or_none()

        if partner_up:

            if partner_logado.id == partner_up.id:
                if partner.name:
                    partner_up.name = partner.name
                if partner.cnpj:
                    partner_up.cnpj = partner.cnpj
                if partner.email:
                    partner_up.email = partner.email
                if partner.password:
                    partner_up.password = gerar_hash_senha(partner.password)

                try:
                    await session.commit()
                    return partner_up
                except IntegrityError:
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                        detail="Já existe um parceiro com esse e-mail ou CNPJ cadastrado.")

            else:
                raise HTTPException(detail='O parceiro logado não tem permissão para modificar este parceiro.',
                                    status_code=status.HTTP_403_FORBIDDEN)
        else:
            raise HTTPException(detail='Parceiro não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE Partner
# Esse endpoint deleta o cadastro de um parceiro, porem o parceiro pode deletar apenas o seu cadastro.
@router.delete('/{partner_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_partner(partner_id: int, db: AsyncSession = Depends(get_session), partner_logado: PartnerModel = Depends(get_current_user)):
    async with db as session:
        query = select(PartnerModel).filter(PartnerModel.id == partner_id)
        result = await session.execute(query)
        partner_del: PartnerModel = result.scalars().unique().one_or_none()

        if partner_del:
            if partner_logado.id == partner_del.id:
                await session.delete(partner_del)
                await session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)

            else:
                raise HTTPException(detail='O parceiro logado não tem permissão para deletar este parceiro.',
                                    status_code=status.HTTP_403_FORBIDDEN)
        else:
            raise HTTPException(detail='Parceiro não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)


# POST Login
# Esse endpoint faz o login dos parceiros, retornando um token de acesso.
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    partner = await autenticar(email=form_data.username, password=form_data.password, db=db)

    if not partner:
        raise HTTPException(detail='Dados de acesso incorretos.',
                            status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"access_token": criar_token_acesso(sub=partner.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
