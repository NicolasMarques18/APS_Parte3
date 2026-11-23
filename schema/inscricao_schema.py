from pydantic import BaseModel
from schema.participante_schema import ParticipanteResponse

class InscricaoResponse(BaseModel):
    id: int
    evento_id: int
    participante_id: int
    data_inscricao: str

    class Config:
        from_attributes = True

class ParticipanteInscritoResponse(ParticipanteResponse):
    data_inscricao: str
