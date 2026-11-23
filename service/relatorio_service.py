from sqlalchemy.orm import Session
from sqlalchemy import func
from model.evento import Evento
from model.participante import Participante
from model.inscricao import Inscricao

def obter_relatorio_ocupacao(db: Session):
    eventos = db.query(Evento).all()
    relatorio = []
    for evento in eventos:
        total_inscritos = len(evento.inscricoes)
        vagas_disponiveis = max(0, evento.capacidade - total_inscritos)
        percentual = round((total_inscritos / evento.capacidade) * 100, 1) if evento.capacidade > 0 else 0.0
        relatorio.append({
            "evento_id": evento.id,
            "titulo": evento.titulo,
            "capacidade": evento.capacidade,
            "total_inscritos": total_inscritos,
            "vagas_disponiveis": vagas_disponiveis,
            "percentual_ocupacao": percentual
        })
    return relatorio

def obter_relatorio_categorias(db: Session):
    categorias_query = db.query(
        Evento.categoria,
        func.count(func.distinct(Evento.id)).label("total_eventos"),
        func.sum(Evento.capacidade).label("capacidade_total")
    ).group_by(Evento.categoria).all()

    relatorio = []
    for cat, total_ev, cap_tot in categorias_query:
        total_inscricoes = db.query(Inscricao).join(Evento).filter(Evento.categoria == cat).count()
        relatorio.append({
            "categoria": cat,
            "total_eventos": total_ev,
            "capacidade_total": cap_tot or 0,
            "total_inscricoes": total_inscricoes
        })
    return relatorio

def obter_relatorio_cursos(db: Session):
    cursos_query = db.query(
        Participante.curso,
        func.count(func.distinct(Participante.id)).label("total_participantes")
    ).group_by(Participante.curso).all()

    relatorio = []
    for curso, total_part in cursos_query:
        total_inscricoes = db.query(Inscricao).join(Participante).filter(Participante.curso == curso).count()
        relatorio.append({
            "curso": curso,
            "total_participantes": total_part,
            "total_inscricoes": total_inscricoes
        })
    return relatorio
