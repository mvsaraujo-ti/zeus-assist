"""
Ask API — ZEUS

Controller fino com:
- Guardrails
- Vault determinístico
- Renderização desacoplada
- Camada conversacional
- Memória curta de contexto
"""

from fastapi import APIRouter

from app.schemas.ask import AskRequest, AskResponse
from app.core.guardrails import validate_question
from app.services.vault_service import search

from app.services.intent_renderer import render_contact
from app.services.system_renderer import render_system
from app.services.flow_renderer import render_flow

from app.services.conversational_service import apply_conversational_layer
from app.services.context_service import save_context, get_context

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_zeus(payload: AskRequest):

    # =====================================================
    # 1️⃣ GUARDRAILS
    # =====================================================
    try:
        validate_question(payload.question)
    except ValueError as e:
        return AskResponse(
            answer=str(e),
            source="rule"
        )

    # =====================================================
    # 2️⃣ BUSCA NO VAULT
    # =====================================================
    result = search(payload.question)

    # =====================================================
    # 3️⃣ SE ACHOU NO VAULT
    # =====================================================
    if result:
        raw = result.get("raw", {})
        item_type = result.get("type")

        # Salva contexto para perguntas subsequentes
        save_context(item_type, raw)

        if item_type == "flow":
            answer = render_flow(raw, payload.question)

        elif item_type == "system":
            answer = render_system(raw, payload.question)

        elif item_type == "contact":
            answer = render_contact(raw, payload.question)

        else:
            answer = "Informação institucional encontrada na base do ZEUS."

        final_answer = apply_conversational_layer(answer)

        return AskResponse(
            answer=final_answer,
            source="vault"
        )

    # =====================================================
    # 4️⃣ NÃO ACHOU → USA MEMÓRIA CURTA
    # =====================================================
    context = get_context()

    if context:
        raw = context.get("last_raw")
        item_type = context.get("last_type")

        if item_type == "flow":
            answer = render_flow(raw, payload.question)

        elif item_type == "system":
            answer = render_system(raw, payload.question)

        elif item_type == "contact":
            answer = render_contact(raw, payload.question)

        else:
            answer = None

        if answer:
            final_answer = apply_conversational_layer(answer)

            return AskResponse(
                answer=final_answer,
                source="context"
            )

    # =====================================================
    # 5️⃣ FALLBACK FINAL
    # =====================================================
    return AskResponse(
        answer=(
            "Não encontrei essa informação na base do ZEUS. "
            "Por favor, abra um chamado para o suporte."
        ),
        source="fallback"
    )
