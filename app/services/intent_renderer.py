"""
Intent Renderer — ZEUS

Responsável por:
- Detectar intenções específicas na pergunta
- Renderizar respostas precisas com base no tipo do item
- Evitar lógica de decisão no ask.py

⚠️ NÃO acessa YAML
⚠️ NÃO decide conteúdo institucional
⚠️ Trabalha apenas com dados já resolvidos pelo Vault
"""

from typing import Optional


# =========================================================
# 🔹 MAPA DE INTENÇÕES PARA CONTATOS
# =========================================================

CONTACT_FIELD_INTENTS = {
    "telefone": "phone",
    "fone": "phone",
    "email": "email",
    "e-mail": "email",
    "horario": "working_hours",
    "horário": "working_hours",
}


# =========================================================
# 🔹 DETECÇÃO DE INTENÇÃO
# =========================================================

def detect_contact_field(question: str) -> Optional[str]:
    """
    Detecta se a pergunta solicita um campo específico de contato.

    Retorna:
    - nome do campo (ex: 'phone', 'email')
    - None se não houver intenção específica
    """
    if not question:
        return None

    q = question.lower()

    for keyword, field in CONTACT_FIELD_INTENTS.items():
        if keyword in q:
            return field

    return None


# =========================================================
# 🔹 RENDERIZAÇÃO DE CONTATO
# =========================================================

def render_contact(raw: dict, question: str) -> str:
    """
    Renderiza resposta de contato com base na intenção detectada.
    """
    sector = raw.get("sector", "Setor de TI")

    field = detect_contact_field(question)

    # -------------------------------
    # 🔹 INTENÇÃO ESPECÍFICA
    # -------------------------------
    if field:
        value = raw.get(field)

        if value:
            labels = {
                "phone": "📞 Telefone",
                "email": "📧 E-mail",
                "working_hours": "⏰ Horário de atendimento",
            }

            label = labels.get(field, "Informação")
            return f"{label} da {sector}: {value}"

        return f"Não há informação de {field} cadastrada para o setor {sector}."

    # -------------------------------
    # 🔹 RESPOSTA COMPLETA (SEM INTENÇÃO)
    # -------------------------------
    lines = [f"📌 **{sector}**"]

    if raw.get("phone"):
        lines.append(f"📞 Telefone: {raw['phone']}")

    if raw.get("email"):
        lines.append(f"📧 E-mail: {raw['email']}")

    channels = raw.get("channels", {})
    if channels:
        lines.append("💬 Canais de atendimento:")
        for name, value in channels.items():
            lines.append(f"- {name.capitalize()}: {value}")

    if raw.get("working_hours"):
        lines.append(f"⏰ Horário de atendimento: {raw['working_hours']}")

    if raw.get("notes"):
        lines.append(f"\nℹ️ {raw['notes']}")

    return "\n".join(lines)
