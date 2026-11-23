from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schema.participante_schema import ParticipanteCreate, ParticipanteUpdate, ParticipanteResponse
from service import participante_service

router = APIRouter(prefix="/participantes", tags=["Participantes"])

@router.post("", response_model=ParticipanteResponse, status_code=status.HTTP_201_CREATED)
def criar_participante(participante: ParticipanteCreate, db: Session = Depends(get_db)):
    return participante_service.criar_participante(db, participante)

@router.get("", response_model=List[ParticipanteResponse])
def listar_participantes(db: Session = Depends(get_db)):
    return participante_service.listar_participantes(db)

@router.get("/{id}", response_model=ParticipanteResponse)
def buscar_participante(id: int, db: Session = Depends(get_db)):
    return participante_service.buscar_participante_por_id(db, id)

@router.put("/{id}", response_model=ParticipanteResponse)
def atualizar_participante(id: int, participante: ParticipanteUpdate, db: Session = Depends(get_db)):
    return participante_service.atualizar_participante(db, id, participante)

@router.delete("/{id}")
def deletar_participante(id: int, db: Session = Depends(get_db)):
    return participante_service.deletar_participante(db, id)
