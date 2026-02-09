from fastapi import APIRouter

from app.schemas.ask import AskRequest, AskResponse
from app.core.guardrails import validate_question, detect_social_intent

from app.services.vault_service import search
from app.services.intent_renderer import render_contact
from app.services.system_renderer import render_system
from app.services.flow_renderer import render_flow

from app.services.context_service import save_context, get_context
from app.services.tone_service import apply_tone
from app.services.meta_responses import zeus_identity
from app.services.suggestions_logger import log_suggestion

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_zeus(payload: AskRequest):
    # =====================================================
    # 0️⃣ NORMALIZAÇÃO BÁSICA
    # =====================================================
    question = payload.question.strip()

    if not question:
        return AskResponse(
            answer=(
                "Olá! 👋\n"
                "Sou o **ZEUS**, assistente institucional de TI do TJMA.\n\n"
                "Como posso te ajudar hoje?"
            ),
            source="social",
        )

    # =====================================================
    # 1️⃣ SOCIAL / META  (SHORT-CIRCUIT ABSOLUTO)
    # =====================================================
    social_intent = detect_social_intent(question)

    # Saudação curta (oi, bom dia, etc.)
    if social_intent == "greeting" and len(question.split()) <= 3:
        return AskResponse(
            answer=(
                "Olá! 👋\n"
                "Sou o **ZEUS**, assistente institucional de TI do TJMA.\n\n"
                "Como posso te ajudar hoje?"
            ),
            source="social",
        )

    # META — identidade do ZEUS
    # ⚠️ NÃO consulta Vault
    # ⚠️ NÃO passa por guardrails
    if social_intent == "meta":
        return AskResponse(
            answer=zeus_identity(),
            source="meta",
        )

    # =====================================================
    # 2️⃣ GUARDRAILS
    # =====================================================
    try:
        validate_question(question)
    except ValueError as e:
        return AskResponse(
            answer=str(e),
            source="rule",
        )

    # =====================================================
    # 3️⃣ BUSCA NO VAULT
    # =====================================================
    result = search(question)

    # -----------------------------------------------------
    # 3.1 ITEM ENCONTRADO (raw presente)
    # -----------------------------------------------------
    if result and "raw" in result:
        raw = result["raw"]
        item_type = result["type"]

        # salva contexto para follow-up
        save_context(item_type, raw)

        if item_type == "flow":
            answer = render_flow(raw, question)
        elif item_type == "system":
            answer = render_system(raw, question)
        elif item_type == "contact":
            answer = render_contact(raw, question)
        else:
            answer = "Informação institucional encontrada na base do ZEUS."

        final_answer = apply_tone(
            text=answer,
            source="vault",
            has_greeting=(social_intent == "greeting"),
            is_followup=False,
        )

        return AskResponse(
            answer=final_answer,
            source="vault",
        )

    # -----------------------------------------------------
    # 3.2 SUGESTÃO EDUCADA (COM LOG)
    # -----------------------------------------------------
    if result and result.get("type") == "suggestion":
        sugestoes = result.get("suggestions", [])[:5]

        # registra para análise futura
        log_suggestion(question, sugestoes)

        sugestoes_txt = ", ".join(sugestoes)

        return AskResponse(
            answer=(
                "Não encontrei exatamente o que você procurava.\n\n"
                f"Talvez você esteja buscando por algo relacionado a: **{sugestoes_txt}**.\n\n"
                "Se quiser, reformule a pergunta ou seja um pouco mais específico."
            ),
            source="fallback",
        )

    # =====================================================
    # 4️⃣ MEMÓRIA CURTA (FOLLOW-UP)
    # =====================================================
    context = get_context()

    if context:
        raw = context.get("last_raw")
        item_type = context.get("last_type")

        if item_type == "flow":
            answer = render_flow(raw, question)
        elif item_type == "system":
            answer = render_system(raw, question)
        elif item_type == "contact":
            answer = render_contact(raw, question)
        else:
            answer = None

        if answer:
            final_answer = apply_tone(
                text=answer,
                source="context",
                is_followup=True,
            )

            return AskResponse(
                answer=final_answer,
                source="context",
            )

    # =====================================================
    # 5️⃣ FALLBACK FINAL
    # =====================================================
    fallback_text = (
        "Não encontrei essa informação na base do ZEUS.\n"
        "Se desejar, posso te orientar sobre como abrir um chamado para o suporte."
    )

    return AskResponse(
        answer=apply_tone(
            text=fallback_text,
            source="fallback",
        ),
        source="fallback",
    )
