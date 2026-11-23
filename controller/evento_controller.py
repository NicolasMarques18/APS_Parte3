from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schema.evento_schema import EventoCreate, EventoUpdate, EventoResponse
from service import evento_service

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post("", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def criar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    return evento_service.criar_evento(db, evento)

@router.get("", response_model=List[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return evento_service.listar_eventos(db)

@router.get("/{id}", response_model=EventoResponse)
def buscar_evento(id: int, db: Session = Depends(get_db)):
    return evento_service.buscar_evento_por_id(db, id)

@router.put("/{id}", response_model=EventoResponse)
def atualizar_evento(id: int, evento: EventoUpdate, db: Session = Depends(get_db)):
    return evento_service.atualizar_evento(db, id, evento)

@router.delete("/{id}")
def deletar_evento(id: int, db: Session = Depends(get_db)):
    return evento_service.deletar_evento(db, id)
