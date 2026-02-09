# app/schemas/ask.py

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """
    DTO de entrada da rota /ask.
    Representa a pergunta enviada pelo usuário.
    """
    question: str = Field(
        ...,
        min_length=1,
        description="Pergunta do usuário para o ZEUS"
    )


class AskResponse(BaseModel):
    """
    DTO de saída da rota /ask.
    """
    answer: str
    source: str  # vault | rule | fallback | social | meta
