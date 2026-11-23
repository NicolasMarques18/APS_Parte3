from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Inscricao(Base):
    __tablename__ = "inscricoes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    evento_id = Column(Integer, ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False)
    participante_id = Column(Integer, ForeignKey("participantes.id", ondelete="CASCADE"), nullable=False)
    data_inscricao = Column(String, nullable=False, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    evento = relationship("Evento", back_populates="inscricoes")
    participante = relationship("Participante", back_populates="inscricoes")

    __table_args__ = (
        UniqueConstraint('evento_id', 'participante_id', name='uq_evento_participante'),
    )
