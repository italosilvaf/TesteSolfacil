from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from core.configs import settings
from core.security import verificar_senha
from pydantic import EmailStr
from models.partner_model import PartnerModel


# Definição do endpoint de login
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl='/partners/login'
)


# Função para a autenticação de usuario(parceiro).
async def autenticar(email: EmailStr, password: str, db: AsyncSession) -> Optional[PartnerModel]:
    async with db as session:
        query = select(PartnerModel).filter(PartnerModel.email == email)
        result = await session.execute(query)
        partner: PartnerModel = result.scalars().unique().one_or_none()

        if not partner:
            return None

        if not verificar_senha(password, partner.password):
            return None

        return partner


# Função interna utilizada para criação de token de acesso.
def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    payload = {}

    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


# Função para criação de token de acesso, utilizando a funçao anterior.
def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINURES),
        sub=sub
    )
