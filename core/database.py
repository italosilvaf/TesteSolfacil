from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from core.configs import settings

# Criação de conexão assíncrona com o banco de dados.
engine: AsyncEngine = create_async_engine(settings.DB_URL)

# Criação de sessões para fazer leitura e escrita no banco de dados.
Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
