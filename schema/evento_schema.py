from pydantic import BaseModel, Field
from typing import Optional

class EventoBase(BaseModel):
    titulo: str = Field(..., min_length=1, description="Título do evento não pode ser vazio.")
    descricao: Optional[str] = None
    data: str = Field(..., min_length=1, description="Data de realização.")
    horario: str = Field(..., min_length=1, description="Horário de realização.")
    local: str = Field(..., min_length=1, description="Local do evento.")
    capacidade: int = Field(..., gt=0, description="A capacidade deve ser maior que zero.")
    categoria: str = Field(..., min_length=1, description="Categoria do evento.")

class EventoCreate(EventoBase):
    pass

class EventoUpdate(EventoBase):
    pass

class EventoResponse(EventoBase):
    id: int

    class Config:
        from_attributes = True
