from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):

    # Url de conexão do banco de dados
    DB_URL: str = 'postgresql+asyncpg://postgres:root@localhost:5432/dbtestesolfacil'
    DBBaseModel = declarative_base()

    # Chave secreta utilizada para assinar tokens JWT
    JWT_SECRET: str = 'cRcg132OnHyMVi0RqKgyjn3xZYH-5nZLyv5YJpPG6a0'
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """

    # Algoritmo utilizado para assinar tokens JWT.
    ALGORITHM: str = 'HS256'

    # Tempo em minutos para a expiração do token: 60 minutos * 24 horas * 7 dias = 1 semana
    ACCESS_TOKEN_EXPIRE_MINURES = 60 * 24 * 7

    class Config:

        # Ativação do case sensitive, ou seja, diferença entre letras maiúsculas e minúsculas.
        case_sensitive = True


settings: Settings = Settings()
