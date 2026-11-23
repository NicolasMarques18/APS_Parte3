from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schema.inscricao_schema import InscricaoResponse, ParticipanteInscritoResponse
from service import inscricao_service

router = APIRouter(tags=["Inscrições"])

@router.post("/eventos/{evento_id}/inscricoes/{participante_id}", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
def inscrever_participante(evento_id: int, participante_id: int, db: Session = Depends(get_db)):
    return inscricao_service.inscrever_participante(db, evento_id, participante_id)

@router.get("/eventos/{evento_id}/inscricoes", response_model=List[ParticipanteInscritoResponse])
def listar_inscritos(evento_id: int, db: Session = Depends(get_db)):
    return inscricao_service.listar_inscritos_por_evento(db, evento_id)
