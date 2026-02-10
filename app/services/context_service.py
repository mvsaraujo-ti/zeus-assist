"""
Context Service — ZEUS

Responsável por:
- Manter memória curta da conversa
- Guardar o último item resolvido (SYSTEM / FLOW / CONTACT)
- Permitir continuidade natural (follow-up)
- Expirar contexto automaticamente (TTL)

⚠️ Memória em RAM (reinício limpa)
⚠️ Não persiste dados
⚠️ Não envolve IA
⚠️ Determinístico, previsível e auditável
"""

from typing import Optional, List, Dict
from time import time
import os


# =========================================================
# 🔹 CONFIGURAÇÃO DE TTL (Time To Live)
# =========================================================

# TTL do contexto em segundos
# Padrão: 180s (3 minutos)
CONTEXT_TTL_SECONDS = int(os.getenv("ZEUS_CONTEXT_TTL", "180"))


# =========================================================
# 🔹 MEMÓRIA EM RAM (CONTEXTO RICO)
# =========================================================

_CONTEXT: Dict = {
    "type": None,          # system | flow | contact
    "system_id": None,     # identificador do sistema
    "system_title": None,  # nome amigável
    "flow_id": None,       # identificador do fluxo (se houver)
    "flow_title": None,    # nome amigável do fluxo
    "raw": None,           # objeto YAML bruto (fonte da verdade)
    "timestamp": None,     # quando foi salvo
}


# =========================================================
# 🔹 FRASES GENÉRICAS DE FOLLOW-UP
# =========================================================
# Essas frases NÃO identificam novo alvo.
# Indicam continuidade do último contexto válido.

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

def save_context(
    item_type: str,
    raw: dict,
    system_id: Optional[str] = None,
    system_title: Optional[str] = None,
    flow_id: Optional[str] = None,
    flow_title: Optional[str] = None,
) -> None:
    """
    Salva o contexto atual com TTL.
    O contexto guarda IDENTIDADE, não texto.
    """

    _CONTEXT.update({
        "type": item_type,
        "system_id": system_id,
        "system_title": system_title,
        "flow_id": flow_id,
        "flow_title": flow_title,
        "raw": raw,
        "timestamp": time(),
    })


def get_context() -> Optional[Dict]:
    """
    Retorna o contexto atual se:
    - existir
    - não estiver expirado
    """

    if not _CONTEXT["type"] or not _CONTEXT["raw"]:
        return None

    if _is_expired():
        clear_context()
        return None

    return _CONTEXT


def clear_context() -> None:
    """
    Limpa completamente o contexto.
    """

    for key in _CONTEXT:
        _CONTEXT[key] = None


# =========================================================
# 🔹 TTL — CONTROLE DE EXPIRAÇÃO
# =========================================================

def _is_expired() -> bool:
    """
    Verifica se o contexto expirou baseado no TTL.
    """

    timestamp = _CONTEXT.get("timestamp")
    if not timestamp:
        return True

    return (time() - timestamp) > CONTEXT_TTL_SECONDS


# =========================================================
# 🔹 DETECÇÃO DE FOLLOW-UP IMPLÍCITO
# =========================================================

def is_followup_only(question_words: List[str]) -> bool:
    """
    Retorna True apenas se a pergunta for:
    - um follow-up genérico
    - SEM identificadores explícitos
    - COM contexto válido (não expirado)
    """

    if not question_words:
        return False

    # Sem contexto válido, não existe follow-up
    if not get_context():
        return False

    question_text = " ".join(question_words)

    # Palavras que indicam novo alvo explícito
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

    # Follow-up só ocorre se for frase genérica pura
    for phrase in FOLLOWUP_GENERIC_PHRASES:
        if phrase in question_text:
            return True

    return False
