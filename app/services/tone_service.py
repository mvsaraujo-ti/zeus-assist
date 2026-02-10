"""
Tone Service — ZEUS

Responsável por:
- Ajustar tom institucional (CUX)
- Aplicar humanização controlada (pós-processamento)
- NÃO decidir conteúdo
"""

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

    source:
    - vault
    - flow
    - system
    - contact
    - fallback
    - suggestion
    - social
    - meta
    """

    # =====================================================
    # 1️⃣ FONTES QUE NÃO DEVEM SER ALTERADAS
    # =====================================================

    if source in {"social", "meta"}:
        return text

    final_text = text

    # =====================================================
    # 2️⃣ AJUSTES DETERMINÍSTICOS DE TOM
    # =====================================================

    if is_followup:
        final_text = f"Complementando a informação anterior:\n\n{final_text}"

    elif has_greeting and source == "vault":
        final_text = f"Bom dia!\n\n{final_text}"

    # =====================================================
    # 3️⃣ HUMANIZAÇÃO SELETIVA (OLLAMA)
    # =====================================================
    # Apenas para respostas de erro/orientação

    if source in {"fallback", "suggestion"}:
        final_text = rewrite_text(final_text)

    return final_text
