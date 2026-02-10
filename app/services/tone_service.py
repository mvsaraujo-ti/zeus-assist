# app/services/tone_service.py

from typing import Optional

from app.services.rewrite_service import rewrite_text


def apply_tone(
    *,
    text: str,
    source: str,
    has_greeting: bool = False,
    is_followup: bool = False
) -> str:
    """
    Aplica a camada de tom (CUX) à resposta final do ZEUS.

    Parâmetros:
    - text: conteúdo já decidido e renderizado
    - source: origem da resposta (vault | context | fallback | social | meta)
    - has_greeting: pergunta original contém saudação?
    - is_followup: resposta vem da memória curta?

    Retorna:
    - texto final com tom adequado (e humanizado, se habilitado)
    """

    # =====================================================
    # 1️⃣ RESPOSTAS QUE NÃO DEVEM SER ALTERADAS
    # =====================================================

    # SOCIAL PURO
    if source == "social":
        return text

    # META (identidade institucional)
    if source == "meta":
        return text

    # =====================================================
    # 2️⃣ CONSTRUÇÃO DO TEXTO BASE (DETERMINÍSTICO)
    # =====================================================

    final_text = text

    # FOLLOW-UP (continuação)
    if is_followup:
        final_text = f"Complementando a informação anterior:\n\n{final_text}"

    # WARM CONTEXTUAL (saudação + pergunta real)
    elif has_greeting and source == "vault":
        final_text = f"Bom dia!\n\n{final_text}"

    # FALLBACK mantém texto neutro
    # VAULT padrão mantém texto como veio

    # =====================================================
    # 3️⃣ HUMANIZAÇÃO OPCIONAL (OLLAMA — POST-PROCESSING)
    # =====================================================

    # ⚠️ Apenas reescrita
    # ⚠️ Sem alterar significado
    # ⚠️ Fail-safe interno
    final_text = rewrite_text(final_text)

    return final_text
