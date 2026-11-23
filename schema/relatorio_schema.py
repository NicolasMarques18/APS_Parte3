from pydantic import BaseModel

class RelatorioOcupacaoResponse(BaseModel):
    evento_id: int
    titulo: str
    capacidade: int
    total_inscritos: int
    vagas_disponiveis: int
    percentual_ocupacao: float

class RelatorioCategoriaResponse(BaseModel):
    categoria: str
    total_eventos: int
    capacidade_total: int
    total_inscricoes: int

class RelatorioCursoResponse(BaseModel):
    curso: str
    total_participantes: int
    total_inscricoes: int
