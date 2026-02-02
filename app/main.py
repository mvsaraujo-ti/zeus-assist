# /home/mvsaraujo@tjma.jus.br/DEV/zeus/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importação das rotas (API v1)
from app.api.v1.ask import router as ask_router

# Criação da aplicação FastAPI
app = FastAPI(
    title="ZEUS - Assistente N1 de TI",
    description="Backend do assistente ZEUS para suporte N1",
    version="1.0.0",
)

# Configuração de CORS
# Importante para permitir acesso do frontend HTML/JS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de healthcheck (boa prática)
@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint simples para verificar se a API está online.
    Usado por monitoramento e testes.
    """
    return {"status": "ok", "service": "ZEUS"}

# Registro das rotas da API versão 1
app.include_router(
    ask_router,
    prefix="/api/v1",
    tags=["Ask"]
)
