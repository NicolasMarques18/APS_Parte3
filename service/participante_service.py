from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from model.participante import Participante
from schema.participante_schema import ParticipanteCreate, ParticipanteUpdate

def criar_participante(db: Session, participante_schema: ParticipanteCreate) -> Participante:
    existente = db.query(Participante).filter(Participante.email == participante_schema.email).first()
    if existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um participante cadastrado com este e-mail.")
    
    novo_participante = Participante(**participante_schema.model_dump())
    db.add(novo_participante)
    db.commit()
    db.refresh(novo_participante)
    return novo_participante

def listar_participantes(db: Session):
    return db.query(Participante).all()

def buscar_participante_por_id(db: Session, participante_id: int) -> Participante:
    participante = db.query(Participante).filter(Participante.id == participante_id).first()
    if not participante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participante não encontrado.")
    return participante

def atualizar_participante(db: Session, participante_id: int, participante_schema: ParticipanteUpdate) -> Participante:
    participante = buscar_participante_por_id(db, participante_id)
    
    email_existente = db.query(Participante).filter(
        Participante.email == participante_schema.email,
        Participante.id != participante_id
    ).first()
    if email_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe um participante cadastrado com este e-mail.")
    
    for key, value in participante_schema.model_dump().items():
        setattr(participante, key, value)
    db.commit()
    db.refresh(participante)
    return participante

def deletar_participante(db: Session, participante_id: int):
    participante = buscar_participante_por_id(db, participante_id)
    db.delete(participante)
    db.commit()
    return {"detail": "Participante excluído com sucesso."}
