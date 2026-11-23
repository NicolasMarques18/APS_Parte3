from fastapi import FastAPI
from database import create_tables
from controller import evento_controller, participante_controller, inscricao_controller, relatorio_controller

# Criar tabelas no banco de dados SQLite na inicialização
create_tables()

app = FastAPI(
    title="API de Gerenciamento de Eventos Acadêmicos",
    description="APS 3 - Persistência e Consolidação de Dados com SQLite, SQLAlchemy e FastAPI",
    version="3.0.0"
)

# Inclusão dos roteadores (controllers)
app.include_router(evento_controller.router)
app.include_router(participante_controller.router)
app.include_router(inscricao_controller.router)
app.include_router(relatorio_controller.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "mensagem": "API de Gestão de Eventos Acadêmicos - APS 3 rodando com sucesso!",
        "documentacao": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
