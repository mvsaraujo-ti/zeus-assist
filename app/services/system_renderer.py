"""
System Renderer — ZEUS

Responsável por:
- Detectar intenção relacionada a sistemas
- Renderizar respostas precisas sobre sistemas
- Evitar lógica condicional no ask.py

⚠️ NÃO acessa YAML
⚠️ NÃO decide busca
⚠️ Usa apenas dados já resolvidos pelo Vault
"""

from typing import Optional


# =========================================================
# 🔹 MAPA DE INTENÇÕES PARA SISTEMAS
# =========================================================

SYSTEM_INTENTS = {
    "acesso": "access",
    "acessar": "access",
    "entrar": "access",
    "login": "access",
    "suporte": "support",
    "responsavel": "support",
    "responsável": "support",
    "quem cuida": "support",
}


# =========================================================
# 🔹 DETECÇÃO DE INTENÇÃO
# =========================================================

def detect_system_intent(question: str) -> Optional[str]:
    """
    Detecta intenção relacionada a sistemas.

    Retorna:
    - 'access'
    - 'support'
    - None
    """
    if not question:
        return None

    q = question.lower()

    for keyword, intent in SYSTEM_INTENTS.items():
        if keyword in q:
            return intent

    return None


# =========================================================
# 🔹 RENDERIZAÇÃO DE SISTEMA
# =========================================================

def render_system(raw: dict, question: str) -> str:
    """
    Renderiza resposta de sistema com base na intenção detectada.
    """
    name = raw.get("name", "Sistema institucional")
    description = raw.get("description", "")

    intent = detect_system_intent(question)

    # -------------------------------
    # 🔹 INTENÇÃO: ACESSO
    # -------------------------------
    if intent == "access":
        access = raw.get("access", {})
        if access:
            lines = [f"🔐 **Acesso ao sistema {name}:**"]
            for key, value in access.items():
                lines.append(f"- {key.capitalize()}: {value}")
            return "\n".join(lines)

        return f"O acesso ao sistema {name} depende das regras institucionais."

    # -------------------------------
    # 🔹 INTENÇÃO: SUPORTE
    # -------------------------------
    if intent == "support":
        support = raw.get("support", {})
        if support:
            lines = [f"🛠️ **Suporte do sistema {name}:**"]
            for key, value in support.items():
                lines.append(f"- {key.capitalize()}: {value}")
            return "\n".join(lines)

        return f"O suporte do sistema {name} é definido pelo setor responsável."

    # -------------------------------
    # 🔹 RESPOSTA PADRÃO
    # -------------------------------
    return f"**{name}**\n\n{description}"
