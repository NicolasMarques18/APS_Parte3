from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schema.relatorio_schema import RelatorioOcupacaoResponse, RelatorioCategoriaResponse, RelatorioCursoResponse
from service import relatorio_service

router = APIRouter(prefix="/relatorios", tags=["Relatórios e Consolidação"])

@router.get("/eventos/ocupacao", response_model=List[RelatorioOcupacaoResponse])
def relatorio_ocupacao(db: Session = Depends(get_db)):
    return relatorio_service.obter_relatorio_ocupacao(db)

@router.get("/eventos/categorias", response_model=List[RelatorioCategoriaResponse])
def relatorio_categorias(db: Session = Depends(get_db)):
    return relatorio_service.obter_relatorio_categorias(db)

@router.get("/participantes/cursos", response_model=List[RelatorioCursoResponse])
def relatorio_cursos(db: Session = Depends(get_db)):
    return relatorio_service.obter_relatorio_cursos(db)
