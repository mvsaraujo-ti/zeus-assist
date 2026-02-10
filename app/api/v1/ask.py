"""
Ask Controller — ZEUS

Responsável por:
- Receber perguntas do usuário
- Resolver intenção
- Orquestrar Vault, Contexto e Renderers
- Garantir continuidade natural da conversa
- Priorizar procedimentos quando houver ação explícita

⚠️ Não decide conteúdo
⚠️ Não usa IA para decisão
"""

from fastapi import APIRouter

from app.schemas.ask import AskRequest, AskResponse
from app.core.guardrails import validate_question, detect_social_intent

from app.services.vault_service import search, normalize_text
from app.services.intent_renderer import render_contact
from app.services.system_renderer import render_system
from app.services.flow_renderer import render_flow

from app.services.context_service import (
    save_context,
    get_context,
    clear_context,
    is_followup_only,
)

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

    question_words = normalize_text(question)

    # =====================================================
    # 1️⃣ SOCIAL / META (SHORT-CIRCUIT)
    # =====================================================
    social_intent = detect_social_intent(question)

    # Saudação curta
    if social_intent == "greeting" and len(question_words) <= 3:
        return AskResponse(
            answer=(
                "Olá! 👋\n"
                "Sou o **ZEUS**, assistente institucional de TI do TJMA.\n\n"
                "Como posso te ajudar hoje?"
            ),
            source="social",
        )

    # Identidade institucional
    if social_intent == "meta":
        return AskResponse(
            answer=zeus_identity(),
            source="meta",
        )

    # =====================================================
    # 2️⃣ FOLLOW-UP IMPLÍCITO (ANTES DO VAULT)
    # =====================================================
    context = get_context()

    if context and is_followup_only(question_words):
        last_raw = context.get("last_raw")
        last_type = context.get("last_type")

        answer = None

        # SYSTEM → pedido de passo a passo → tentar FLOW relacionado
        if last_type == "system":
            flow_result = search(last_raw.get("title", ""))

            if flow_result and flow_result.get("type") == "flow":
                save_context("flow", flow_result["raw"])
                answer = render_flow(flow_result["raw"], question)
            else:
                answer = (
                    "No momento, não encontrei um passo a passo específico "
                    "para esse sistema."
                )

        # FLOW → reaplica normalmente
        elif last_type == "flow":
            answer = render_flow(last_raw, question)

        # CONTACT → reaplica contato
        elif last_type == "contact":
            answer = render_contact(last_raw, question)

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
    # 3️⃣ GUARDRAILS
    # =====================================================
    try:
        validate_question(question)
    except ValueError as e:
        return AskResponse(
            answer=str(e),
            source="rule",
        )

    # =====================================================
    # 4️⃣ BUSCA NO VAULT
    # =====================================================
    result = search(question)

    # -----------------------------------------------------
    # 4.1 ITEM ENCONTRADO (COM PRIORIDADE DE FLOW)
    # -----------------------------------------------------
    if result and "raw" in result:
        raw = result["raw"]
        item_type = result["type"]

        # 🔁 Se veio SYSTEM mas a pergunta indica ação,
        # tenta promover para FLOW antes de responder
        if item_type == "system":
            ACTION_WORDS = {
                "cadastrar",
                "cadastro",
                "acessar",
                "acesso",
                "solicitar",
                "solicitacao",
                "passo",
                "passos",
            }

            if any(word in question_words for word in ACTION_WORDS):
                flow_result = search(raw.get("title", ""))

                if flow_result and flow_result.get("type") == "flow":
                    raw = flow_result["raw"]
                    item_type = "flow"

        # 🔐 Salva contexto já com o tipo correto
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
    # 4.2 SUGESTÃO EDUCADA
    # -----------------------------------------------------
    if result and result.get("type") == "suggestion":
        suggestions = result.get("suggestions", [])[:5]

        log_suggestion(question, suggestions)

        suggestions_txt = ", ".join(suggestions)

        answer = (
            "Não encontrei exatamente o que você procurava.\n\n"
            f"Talvez você esteja buscando por algo relacionado a: "
            f"**{suggestions_txt}**.\n\n"
            "Se quiser, reformule a pergunta ou seja um pouco mais específico."
        )

        final_answer = apply_tone(
            text=answer,
            source="suggestion",
        )

        return AskResponse(
            answer=final_answer,
            source="suggestion",
        )

    # =====================================================
    # 5️⃣ FALLBACK FINAL
    # =====================================================
    clear_context()

    fallback_text = (
        "Não encontrei essa informação na base do ZEUS.\n"
        "Se desejar, posso te orientar sobre como abrir um chamado para o suporte."
    )

    final_answer = apply_tone(
        text=fallback_text,
        source="fallback",
    )

    return AskResponse(
        answer=final_answer,
        source="fallback",
    )
