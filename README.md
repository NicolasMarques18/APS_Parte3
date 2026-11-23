# APS 3 — Persistência e Consolidação de Dados com SQLite, SQLAlchemy e FastAPI

## 1. Descrição do Projeto
Esta aplicação é uma evolução da API RESTful de gestão de eventos acadêmicos desenvolvida na Avaliação Parcial 02 (APS 2). 

Nesta versão (APS 3), o armazenamento em memória foi substituído pela **persistência de dados relacional** utilizando **SQLite** e **SQLAlchemy ORM**, garantindo que todas as informações de eventos, participantes e inscrições sejam mantidas após o encerramento ou reinicialização da aplicação. Além disso, a API oferece **rotas de consolidação e relatórios estatísticos** desenvolvidos com consultas agregadas dinâmicas em SQLAlchemy.

A arquitetura adota rigorosamente o padrão **MVC (Model-View-Controller)** com separação em camadas (`Controller`, `Service`, `Model`, `Schema` e `Database`).

---

## 2. Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **ORM:** SQLAlchemy
- **Banco de Dados:** SQLite (arquivo `aps3.db`)
- **Validação de Dados:** Pydantic (v2) / `email-validator`
- **Documentação Interativa:** Swagger UI / ReDoc (integrados ao FastAPI)

---

## 3. Estrutura do Projeto

```text
APS_Parte3/
├── main.py                  # Ponto de entrada da aplicação e inicialização do banco
├── database.py              # Configuração da conexão SQLite, SessionLocal e Base do SQLAlchemy
├── requirements.txt         # Dependências do projeto
├── README.md                # Documentação detalhada da aplicação
├── controller/              # Camada Controller (Rotas HTTP e Handlers)
│   ├── __init__.py
│   ├── evento_controller.py
│   ├── participante_controller.py
│   ├── inscricao_controller.py
│   └── relatorio_controller.py
├── model/                   # Camada Model (Mapeamento ORM SQLAlchemy)
│   ├── __init__.py
│   ├── evento.py
│   ├── participante.py
│   └── inscricao.py
├── schema/                  # Camada Schema (Modelos de Validação Pydantic)
│   ├── __init__.py
│   ├── evento_schema.py
│   ├── participante_schema.py
│   ├── inscricao_schema.py
│   └── relatorio_schema.py
└── service/                 # Camada Service (Regras de Negócio e Consultas de Banco)
    ├── __init__.py
    ├── evento_service.py
    ├── participante_service.py
    ├── inscricao_service.py
    └── relatorio_service.py
```

---

## 4. Configuração do Banco de Dados
A conexão com o banco de dados é gerenciada no arquivo `database.py`:
- **Engine:** `create_engine("sqlite:///./aps3.db", connect_args={"check_same_thread": False})`
- **Gerenciamento de Sessão:** A função `get_db()` utiliza um gerador (`yield`) com escopo por requisição HTTP, garantindo que o `db.close()` seja invocado no bloco `finally` após a conclusão de cada requisição.
- **Criação de Tabelas:** O método `Base.metadata.create_all(bind=engine)` é invocado na inicialização da aplicação no `main.py`, criando automaticamente as tabelas `eventos`, `participantes` e `inscricoes` caso elas não existam.
- **Arquivo do Banco:** O arquivo `aps3.db` é gerado na raiz do projeto ao executar a aplicação.

---

## 5. Instruções de Instalação e Execução

### Pré-requisitos
- Python 3.9 ou superior instalado.

### Passo 1: Clonar / Extrair o Projeto
Navegue até a pasta do projeto:
```bash
cd APS_Parte3
```

### Passo 2: Criar e Ativar Ambiente Virtual (Recomendado)
- **Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Passo 3: Instalar as Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Executar a API
```bash
uvicorn main:app --reload
```
A API estará acessível em: `http://127.0.0.1:8000`

---

## 6. Documentação Interativa (Swagger)
Acesse no navegador:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 7. Rotas da API e Exemplos de Uso

### 7.1. Eventos (`/eventos`)
- `POST /eventos` — Cadastrar novo evento
- `GET /eventos` — Listar todos os eventos
- `GET /eventos/{id}` — Buscar evento por ID
- `PUT /eventos/{id}` — Atualizar dados de um evento
- `DELETE /eventos/{id}` — Excluir evento (Remove inscrições associadas via Cascade)

**Exemplo Payload (POST /eventos):**
```json
{
  "titulo": "Introdução à Inteligência Artificial",
  "descricao": "Palestra sobre o impacto do Machine Learning na indústria.",
  "data": "2026-11-25",
  "horario": "19:00",
  "local": "Auditório Principal",
  "capacidade": 100,
  "categoria": "Palestra"
}
```

### 7.2. Participantes (`/participantes`)
- `POST /participantes` — Cadastrar novo participante (E-mail único)
- `GET /participantes` — Listar todos os participantes
- `GET /participantes/{id}` — Buscar participante por ID
- `PUT /participantes/{id}` — Atualizar participante
- `DELETE /participantes/{id}` — Excluir participante (Remove inscrições associadas via Cascade)

**Exemplo Payload (POST /participantes):**
```json
{
  "nome": "Nicolas Vieira Marques",
  "email": "nicolas.marques@aluno.unisenai.edu.br",
  "curso": "Engenharia de Software"
}
```

### 7.3. Inscrições (`/eventos/.../inscricoes`)
- `POST /eventos/{evento_id}/inscricoes/{participante_id}` — Realizar inscrição
  - **Validações:**
    - Evento existe (404 caso não exista).
    - Participante existe (404 caso não exista).
    - Inscrição duplicada (409 Conflict se já cadastrado).
    - Vagas disponíveis (409 Conflict se `total_inscritos >= capacidade`).
- `GET /eventos/{evento_id}/inscricoes` — Listar participantes inscritos em um evento.

### 7.4. Relatórios e Consolidação (`/relatorios`)

#### 1. Relatório de Ocupação dos Eventos (`GET /relatorios/eventos/ocupacao`)
Retorna a capacidade, total de inscritos, vagas restantes e percentual de ocupação de cada evento cadastrado.
**Exemplo Resposta JSON:**
```json
[
  {
    "evento_id": 1,
    "titulo": "Introdução à Inteligência Artificial",
    "capacidade": 100,
    "total_inscritos": 75,
    "vagas_disponiveis": 25,
    "percentual_ocupacao": 75.0
  },
  {
    "evento_id": 2,
    "titulo": "Workshop de Python",
    "capacidade": 40,
    "total_inscritos": 40,
    "vagas_disponiveis": 0,
    "percentual_ocupacao": 100.0
  }
]
```

#### 2. Relatório por Categoria (`GET /relatorios/eventos/categorias`)
Consolida os eventos por categoria (Palestra, Workshop, Minicurso, etc.), calculando o total de eventos, capacidade agregada e número total de inscrições.
**Exemplo Resposta JSON:**
```json
[
  {
    "categoria": "Palestra",
    "total_eventos": 5,
    "capacidade_total": 500,
    "total_inscricoes": 320
  },
  {
    "categoria": "Workshop",
    "total_eventos": 3,
    "capacidade_total": 120,
    "total_inscricoes": 95
  }
]
```

#### 3. Relatório por Curso (`GET /relatorios/participantes/cursos`)
Agrupa as inscrições pelo curso do aluno, calculando a quantidade de alunos cadastrados por curso (sem duplicidade) e o total de inscrições efetuadas.
**Exemplo Resposta JSON:**
```json
[
  {
    "curso": "Engenharia de Software",
    "total_participantes": 80,
    "total_inscricoes": 150
  },
  {
    "curso": "Análise e Desenvolvimento de Sistemas",
    "total_participantes": 60,
    "total_inscricoes": 105
  }
]
```

---

## 8. Guia de Testes e Demonstração dos Cenários (Seção 11)

Para testar os 12 cenários exigidos pelo professor, siga os passos abaixo via Swagger (`/docs`):

1. **Cadastro de Evento:** `POST /eventos` com capacidade 2 (Ex: "Palestra IA").
2. **Cadastro de Participantes:** `POST /participantes` para dois ou três alunos.
3. **Inscrição Normal:** `POST /eventos/1/inscricoes/1` e `POST /eventos/1/inscricoes/2`.
4. **Tentativa de Inscrição Duplicada:** `POST /eventos/1/inscricoes/1` novamente. Retornará HTTP **409 Conflict** (`"Participante já está inscrito neste evento."`).
5. **Tentativa de Inscrição sem Vagas:** `POST /eventos/1/inscricoes/3`. Retornará HTTP **409 Conflict** (`"Não existem vagas disponíveis para este evento."`).
6. **Tentativa em Evento Inexistente:** `POST /eventos/999/inscricoes/1`. Retornará HTTP **404 Not Found**.
7. **Verificação dos Relatórios:** 
   - Teste `GET /relatorios/eventos/ocupacao` e veja a ocupação em 100%.
   - Teste `GET /relatorios/eventos/categorias`.
   - Teste `GET /relatorios/participantes/cursos`.
8. **Persistência dos Dados:** Encerre o Uvicorn (`Ctrl + C`) e inicie novamente. Faça um `GET /eventos` ou `GET /participantes` para comprovar que os dados permanecem gravados no arquivo `aps3.db`.
