"""
Intent Renderer — ZEUS

Responsável por:
- Detectar intenções específicas na pergunta
- Renderizar respostas precisas para contatos
- Trabalhar apenas com dados já resolvidos pelo Vault

⚠️ NÃO acessa YAML
⚠️ NÃO decide busca
"""

from typing import Optional


# =========================================================
# 🔹 MAPA DE INTENÇÕES PARA CONTATOS
# =========================================================

CONTACT_FIELD_INTENTS = {
    "telefone": "phone",
    "fone": "phone",
    "ramal": "ramal",
    "email": "email",
    "e-mail": "email",
    "horario": "hours",
    "horário": "hours",
}


# =========================================================
# 🔹 DETECÇÃO DE INTENÇÃO
# =========================================================

def detect_contact_field(question: str) -> Optional[str]:
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
    name = raw.get("name", "Setor institucional")
    channels = raw.get("channels", {})
    hours = raw.get("hours")

    field = detect_contact_field(question)

    # -----------------------------------------------------
    # 🔹 INTENÇÃO ESPECÍFICA
    # -----------------------------------------------------
    if field:
        if field == "hours" and hours:
            return f"⏰ Horário de atendimento da **{name}**: {hours}"

        value = channels.get(field)

        if value:
            labels = {
                "phone": "📞 Telefone",
                "ramal": "☎️ Ramal",
                "email": "📧 E-mail",
            }
            label = labels.get(field, "Contato")
            return f"{label} da **{name}**: {value}"

        return (
            f"Não encontrei informação de **{field}** para **{name}**.\n"
            f"Você pode pedir o *contato completo*."
        )

    # -----------------------------------------------------
    # 🔹 RESPOSTA COMPLETA (SEM INTENÇÃO)
    # -----------------------------------------------------
    lines = [f"📌 **{name}**"]

    if channels.get("phone"):
        lines.append(f"📞 Telefone: {channels['phone']}")

    if channels.get("ramal"):
        lines.append(f"☎️ Ramal: {channels['ramal']}")

    if channels.get("email"):
        lines.append(f"📧 E-mail: {channels['email']}")

    if hours:
        lines.append(f"⏰ Horário: {hours}")

    return "\n".join(lines)
