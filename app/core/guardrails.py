"""
Guardrails — ZEUS

Responsável por:
- Bloquear perguntas fora do escopo institucional
- Permitir consultas objetivas (lookup), mesmo curtas
- Tratar mensagens sociais (saudações, identidade)
- Evitar uso indevido do assistente

⚠️ NÃO decide respostas de domínio
⚠️ NÃO faz inferência complexa
⚠️ Atua APENAS como filtro e classificador inicial
"""

import re
from typing import Optional


# =========================================================
# 🔹 PALAVRAS FORA DO ESCOPO INSTITUCIONAL
# =========================================================

FORBIDDEN_KEYWORDS = {
    "lei",
    "artigo",
    "processo judicial",
    "jurídico",
    "sentença",
    "acórdão",
    "habeas",
    "recurso",
    "petição",
}


# =========================================================
# 🔹 PALAVRAS DE LOOKUP DIRETO
# =========================================================

LOOKUP_KEYWORDS = {
    "telefone",
    "fone",
    "email",
    "e-mail",
    "horario",
    "horário",
    "contato",
    "whatsapp",
    "telegram",
    "suporte",
    "ramal",
}


# =========================================================
# 🔹 SAUDAÇÕES / SOCIAL (HUMANIZAÇÃO CONTROLADA)
# =========================================================

GREETING_KEYWORDS = {
    "oi",
    "olá",
    "ola",
    "bom dia",
    "boa tarde",
    "boa noite",
    "e aí",
    "eai",
    "fala",
}


# =========================================================
# 🔹 META / IDENTIDADE DO ASSISTENTE
# =========================================================

META_PATTERNS = {
    "quem é você",
    "quem voce é",
    "o que você é",
    "o que voce é",
    "qual seu nome",
    "quem é o zeus",
    "o que é o zeus",
    "pra que você serve",
    "pra que voce serve",
}


# =========================================================
# 🔹 FUNÇÕES PÚBLICAS
# =========================================================

def validate_question(question: str) -> None:
    """
    Valida se a pergunta está dentro do escopo do ZEUS.
    Lança ValueError apenas quando deve BLOQUEAR.
    """

    if not question or not isinstance(question, str):
        raise ValueError("Pergunta inválida.")

    text = question.lower().strip()

    # Bloqueio de temas fora do escopo
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in text:
            raise ValueError(
                "Questões jurídicas não são respondidas pelo ZEUS. "
                "Por favor, abra um chamado para o setor responsável."
            )

    # Normalização simples
    words = re.sub(r"[^\w\s]", "", text).split()

    # Permitir lookup direto (mesmo curto)
    if any(word in LOOKUP_KEYWORDS for word in words):
        return

    # Bloquear frases curtas genéricas (que não sejam sociais)
    if len(words) < 3 and not is_greeting(text):
        raise ValueError(
            "Por favor, informe um pouco mais de contexto para que eu possa ajudar."
        )


def detect_social_intent(question: str) -> Optional[str]:
    """
    Detecta intenção social/meta.
    Retorna:
      - 'greeting'
      - 'meta'
      - None
    """

    q = question.lower().strip()

    if any(p in q for p in META_PATTERNS):
        return "meta"

    if is_greeting(q):
        return "greeting"

    return None


# =========================================================
# 🔹 FUNÇÕES AUXILIARES
# =========================================================

def is_greeting(text: str) -> bool:
    return any(greet == text or greet in text for greet in GREETING_KEYWORDS)
