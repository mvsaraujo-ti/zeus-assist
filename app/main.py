from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =========================================================
# 🔹 IMPORTAÇÃO DAS ROTAS (API v1)
# =========================================================
# Cada router cuida do seu próprio domínio
# main.py apenas registra
from app.api.v1.ask import router as ask_router
from app.api.v1.admin import router as admin_router


# =========================================================
# 🔹 CRIAÇÃO DA APLICAÇÃO FASTAPI
# =========================================================
app = FastAPI(
    title="ZEUS - Assistente N1 de TI",
    description="Backend do assistente ZEUS para suporte N1",
    version="1.0.0",
)


# =========================================================
# 🔹 CONFIGURAÇÃO DE CORS
# =========================================================
# Necessário para permitir chamadas do frontend (HTML/JS)
# Em produção, restringir allow_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Em produção, definir domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# 🔹 HEALTHCHECK
# =========================================================
# Endpoint simples para monitoramento e testes
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "ZEUS"
    }


# =========================================================
# 🔹 REGISTRO DAS ROTAS DA API
# =========================================================

# 🔸 Rotas públicas (usuário final)
app.include_router(
    ask_router,
    prefix="/api/v1",
    tags=["Ask"]
)

# 🔸 Rotas administrativas (alimentação do Vault)
app.include_router(
    admin_router,
    prefix="/api/v1/admin",
    tags=["Admin"]
)
