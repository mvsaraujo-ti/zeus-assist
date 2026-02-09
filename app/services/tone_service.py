# app/services/tone_service.py

from typing import Optional


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
    - texto final com tom adequado
    """

    # SOCIAL PURO
    if source == "social":
        return text

    # META (identidade do ZEUS)
    if source == "meta":
        return text

    # FOLLOW-UP (continuação)
    if is_followup:
        return f"Complementando a informação anterior:\n\n{text}"

    # FALLBACK
    if source == "fallback":
        return text

    # WARM CONTEXTUAL (saudação + pergunta real)
    if has_greeting and source == "vault":
        return f"Bom dia!\n\n{text}"

    # NEUTRO (default)
    return text
