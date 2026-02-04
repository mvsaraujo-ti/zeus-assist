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
    # acesso / login
    "acesso": "access",
    "acessar": "access",
    "entrar": "access",
    "login": "access",
    "logar": "access",

    # suporte / responsável
    "suporte": "support",
    "responsavel": "support",
    "responsável": "support",
    "quem cuida": "support",
    "quem responde": "support",
    "quem é o suporte": "support",
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
    access = raw.get("access", {}) or {}
    support = raw.get("support", {}) or {}

    intent = detect_system_intent(question)

    # -----------------------------------------------------
    # 🔹 INTENÇÃO: ACESSO
    # -----------------------------------------------------
    if intent == "access":
        if access:
            lines = [f"🔐 **Acesso ao sistema {name}:**"]

            if access.get("url"):
                lines.append(f"- 🌐 Endereço: {access['url']}")

            if access.get("login_required") is not None:
                if access["login_required"]:
                    lines.append("- 🔑 Requer login institucional")
                else:
                    lines.append("- 🔓 Acesso sem autenticação")

            if access.get("notes"):
                lines.append(f"- ℹ️ {access['notes']}")

            return "\n".join(lines)

        return (
            f"O acesso ao sistema **{name}** "
            f"segue as normas institucionais vigentes."
        )

    # -----------------------------------------------------
    # 🔹 INTENÇÃO: SUPORTE
    # -----------------------------------------------------
    if intent == "support":
        if support:
            lines = [f"🛠️ **Suporte do sistema {name}:**"]

            if support.get("sector"):
                lines.append(f"- 📌 Setor responsável: {support['sector']}")

            if support.get("email"):
                lines.append(f"- 📧 E-mail: {support['email']}")

            if support.get("phone"):
                lines.append(f"- 📞 Telefone: {support['phone']}")

            return "\n".join(lines)

        return (
            f"O suporte do sistema **{name}** "
            f"é prestado pelo setor responsável."
        )

    # -----------------------------------------------------
    # 🔹 RESPOSTA PADRÃO (SEM INTENÇÃO ESPECÍFICA)
    # -----------------------------------------------------
    lines = [f"💻 **{name}**"]

    if description:
        lines.append(f"\n{description}")

    if access:
        lines.append("\n🔐 **Acesso:**")
        if access.get("url"):
            lines.append(f"- 🌐 {access['url']}")
        if access.get("login_required"):
            lines.append("- 🔑 Requer login institucional")

    return "\n".join(lines)
