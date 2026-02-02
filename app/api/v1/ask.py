# app/api/v1/ask.py

from fastapi import APIRouter

from app.schemas.ask import AskRequest, AskResponse
from app.core.guardrails import validate_question
from app.services.vault_service import search_flows
from app.services.ai_service import enhance_answer

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_zeus(payload: AskRequest):
    """
    Endpoint principal do ZEUS.

    Fluxo:
    1. Aplica guardrails (regras de segurança)
    2. Busca fluxo relevante no vault (fonte da verdade)
    3. Usa IA apenas para FORMATAÇÃO da resposta
    4. Retorna resposta segura
    """

    # 1️⃣ Guardrails
    try:
        validate_question(payload.question)
    except ValueError as e:
        return AskResponse(
            answer=str(e),
            source="rule"
        )

    # 2️⃣ Busca no vault
    flow = search_flows(payload.question)

    if flow:
        answer = flow.get(
            "description",
            "Fluxo encontrado na base do ZEUS."
        )

        # Inclui passos, se existirem
        if flow.get("steps"):
            steps = "\n".join(f"- {step}" for step in flow["steps"])
            answer = f"{answer}\n\nPassos:\n{steps}"

        # 3️⃣ IA apenas para melhorar a forma do texto
        formatted_answer = enhance_answer(answer)

        return AskResponse(
            answer=formatted_answer,
            source="vault"
        )

    # 4️⃣ Fallback seguro
    return AskResponse(
        answer=(
            "Não encontrei essa informação na base do ZEUS. "
            "Por favor, abra um chamado para o suporte."
        ),
        source="fallback"
    )
