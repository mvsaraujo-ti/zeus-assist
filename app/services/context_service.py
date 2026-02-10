"""
Context Service — ZEUS

Responsável por:
- Manter memória curta da conversa
- Guardar o último item resolvido
- Permitir continuidade natural (ex: "e o telefone?", "quero o passo a passo")

⚠️ Memória em RAM (reinício limpa)
⚠️ Não persiste dados
⚠️ Não envolve IA
⚠️ Determinístico e auditável
"""

from typing import Optional, List


# =========================================================
# 🔹 MEMÓRIA SIMPLES EM RAM
# =========================================================

# Estrutura mínima de contexto
_CONTEXT = {
    "last_type": None,   # system | flow | contact
    "last_raw": None,    # objeto YAML bruto
}


# =========================================================
# 🔹 FRASES GENÉRICAS DE FOLLOW-UP
# =========================================================
# Essas frases NÃO identificam um novo item.
# Elas indicam continuidade do último contexto válido.

FOLLOWUP_GENERIC_PHRASES = {
    "passo a passo",
    "como fazer",
    "como faco",
    "me ajuda",
    "me ajude",
    "me explique",
    "quero saber",
    "quero ver",
    "como funciona",
    "detalhe",
    "detalhes",
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


# =========================================================
# 🔹 DETECÇÃO DE FOLLOW-UP IMPLÍCITO
# =========================================================

def is_followup_only(question_words: List[str]) -> bool:
    """
    Retorna True apenas se a pergunta for um follow-up genérico,
    SEM novos identificadores relevantes.
    """

    if not question_words:
        return False

    question_text = " ".join(question_words)

    # Se contém palavras que indicam novo alvo, NÃO é follow-up
    IDENTIFIER_WORDS = {
        "sistema",
        "sentinela",
        "mentorh",
        "pje",
        "cadastro",
        "acesso",
    }

    if any(word in question_words for word in IDENTIFIER_WORDS):
        return False

    # Só é follow-up se for frase genérica pura
    for phrase in FOLLOWUP_GENERIC_PHRASES:
        if phrase in question_text:
            return True

    return False

