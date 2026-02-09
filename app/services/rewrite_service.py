import os
import requests
import logging
from typing import Optional

# =====================================================
# CONFIGURAÇÕES
# =====================================================

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "1.5"))

# Flag global de ativação (governança)
REWRITE_ENABLED = os.getenv("ZEUS_REWRITE_ENABLED", "false").lower() == "true"

logger = logging.getLogger("zeus.rewrite")


# =====================================================
# PROMPT INSTITUCIONAL (FIXO E AUDITÁVEL)
# =====================================================

SYSTEM_PROMPT = (
    "Você é um assistente institucional de TI.\n"
    "Sua tarefa é reescrever o texto fornecido mantendo exatamente o mesmo significado.\n\n"
    "REGRAS OBRIGATÓRIAS:\n"
    "- NÃO adicione informações\n"
    "- NÃO remova informações\n"
    "- NÃO altere nomes, números, links ou dados técnicos\n"
    "- NÃO resuma\n"
    "- NÃO explique\n"
    "- NÃO crie exemplos\n\n"
    "Você pode apenas melhorar a fluidez, educação e naturalidade do texto.\n"
)


# =====================================================
# FUNÇÃO PRINCIPAL
# =====================================================

def rewrite_text(text: str) -> str:
    """
    Reescreve o texto de forma mais natural e humana,
    mantendo 100% do significado original.

    Fail-safe: em qualquer erro, retorna o texto original.
    """

    # -------------------------------------------------
    # Guard clauses
    # -------------------------------------------------
    if not REWRITE_ENABLED:
        return text

    if not text or len(text.strip()) < 10:
        return text

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        "stream": False,
    }

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json=payload,
            timeout=OLLAMA_TIMEOUT,
        )

        if response.status_code != 200:
            logger.warning(
                "Rewrite skipped (status %s)", response.status_code
            )
            return text

        data = response.json()
        rewritten = (
            data.get("message", {})
            .get("content", "")
            .strip()
        )

        # Segurança extra: se o modelo devolver algo estranho
        if not rewritten or len(rewritten) < 5:
            return text

        return rewritten

    except requests.exceptions.Timeout:
        logger.warning("Rewrite timeout — returning original text")
        return text

    except Exception as e:
        logger.error("Rewrite error: %s", e)
        return text
