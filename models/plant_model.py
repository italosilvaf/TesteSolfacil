from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from uuid import uuid4
from core.configs import settings


# Models das usinas
class PlantModel(settings.DBBaseModel):
    __tablename__ = "plants"

    uuid = Column(UUID(as_uuid=True), primary_key=True,
                  default=uuid4, unique=True, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cep = Column(String(8), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacidade_maxima_GW = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    partner_id = Column(Integer, ForeignKey('partners.id'))
    criador = relationship(
        "PartnerModel", back_populates='plants', lazy='joined'
    )

    # Função para formatação da data de criação da usina no formato 'AAAA-MM-DD HH:MM:SS'
    @property
    def created_at_formatted(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    # Função para formatação da data de edição da usina no formato 'AAAA-MM-DD HH:MM:SS'
    @property
    def updated_at_formatted(self):
        if self.updated_at:
            return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None
