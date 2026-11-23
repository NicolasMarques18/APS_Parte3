from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from model.evento import Evento
from schema.evento_schema import EventoCreate, EventoUpdate

def criar_evento(db: Session, evento_schema: EventoCreate) -> Evento:
    novo_evento = Evento(**evento_schema.model_dump())
    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)
    return novo_evento

def listar_eventos(db: Session):
    return db.query(Evento).all()

def buscar_evento_por_id(db: Session, evento_id: int) -> Evento:
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    return evento

def atualizar_evento(db: Session, evento_id: int, evento_schema: EventoUpdate) -> Evento:
    evento = buscar_evento_por_id(db, evento_id)
    for key, value in evento_schema.model_dump().items():
        setattr(evento, key, value)
    db.commit()
    db.refresh(evento)
    return evento

def deletar_evento(db: Session, evento_id: int):
    evento = buscar_evento_por_id(db, evento_id)
    db.delete(evento)
    db.commit()
    return {"detail": "Evento excluído com sucesso."}
