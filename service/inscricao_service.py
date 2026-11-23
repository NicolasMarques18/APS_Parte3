from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from model.evento import Evento
from model.participante import Participante
from model.inscricao import Inscricao

def inscrever_participante(db: Session, evento_id: int, participante_id: int) -> Inscricao:
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    
    participante = db.query(Participante).filter(Participante.id == participante_id).first()
    if not participante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participante não encontrado.")
    
    inscricao_existente = db.query(Inscricao).filter(
        Inscricao.evento_id == evento_id,
        Inscricao.participante_id == participante_id
    ).first()
    if inscricao_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Participante já está inscrito neste evento.")
    
    total_inscritos = db.query(Inscricao).filter(Inscricao.evento_id == evento_id).count()
    if total_inscritos >= evento.capacidade:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Não existem vagas disponíveis para este evento.")
    
    nova_inscricao = Inscricao(evento_id=evento_id, participante_id=participante_id)
    db.add(nova_inscricao)
    db.commit()
    db.refresh(nova_inscricao)
    return nova_inscricao

def listar_inscritos_por_evento(db: Session, evento_id: int):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    
    inscricoes = db.query(Inscricao).filter(Inscricao.evento_id == evento_id).all()
    resultado = []
    for i in inscricoes:
        part_dict = {
            "id": i.participante.id,
            "nome": i.participante.nome,
            "email": i.participante.email,
            "curso": i.participante.curso,
            "data_inscricao": i.data_inscricao
        }
        resultado.append(part_dict)
    return resultado
