"""
Context Service — ZEUS

Responsável por:
- Manter memória curta da conversa
- Guardar o último item resolvido
- Permitir continuidade natural (ex: "e o telefone?")

⚠️ Memória em RAM (reinício limpa)
⚠️ Não persiste dados
⚠️ Não envolve IA
"""

from typing import Optional

# =========================================================
# 🔹 MEMÓRIA SIMPLES EM RAM
# =========================================================

_CONTEXT = {
    "last_type": None,
    "last_raw": None,
}


# =========================================================
# 🔹 API DO CONTEXTO
# =========================================================

def save_context(item_type: str, raw: dict) -> None:
    """
    Salva o último item resolvido no contexto.
    """
    _CONTEXT["last_type"] = item_type
    _CONTEXT["last_raw"] = raw


def get_context() -> Optional[dict]:
    """
    Retorna o contexto atual, se existir.
    """
    if _CONTEXT["last_type"] and _CONTEXT["last_raw"]:
        return _CONTEXT
    return None


def clear_context() -> None:
    """
    Limpa completamente o contexto.
    """
    _CONTEXT["last_type"] = None
    _CONTEXT["last_raw"] = None
