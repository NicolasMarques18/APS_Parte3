from pydantic import BaseModel, EmailStr, Field

class ParticipanteBase(BaseModel):
    nome: str = Field(..., min_length=1, description="Nome do participante não pode ser vazio.")
    email: EmailStr = Field(..., description="E-mail válido do participante.")
    curso: str = Field(..., min_length=1, description="Curso do participante.")

class ParticipanteCreate(ParticipanteBase):
    pass

class ParticipanteUpdate(ParticipanteBase):
    pass

class ParticipanteResponse(ParticipanteBase):
    id: int

    class Config:
        from_attributes = True
