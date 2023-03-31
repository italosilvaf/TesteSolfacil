from sqlalchemy import String, Column, DateTime, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from core.configs import settings


# Models dos parceiros
class PartnerModel(settings.DBBaseModel):
    __tablename__ = 'partners'

    uuid = Column(UUID(as_uuid=True), primary_key=True,
                  default=uuid4, unique=True, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(256), nullable=True)
    cnpj = Column(String(14), unique=True, nullable=False)
    email = Column(String(256), index=True, nullable=True, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    plants = relationship(
        "PlantModel",
        cascade="all,delete-orphan",
        back_populates="criador",
        uselist=True,
        lazy="joined"
    )

    # Função para formatação da data de criação do parceiro no formato 'AAAA-MM-DD HH:MM:SS'
    @property
    def created_at_formatted(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    # Função para formatação da data de edição do parceiro no formato 'AAAA-MM-DD HH:MM:SS'
    @property
    def updated_at_formatted(self):
        if self.updated_at:
            return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None
