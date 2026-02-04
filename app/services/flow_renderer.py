"""
Flow Renderer — ZEUS

Responsável por:
- Renderizar fluxos institucionais (procedimentos)
- Diferenciar resumo x passo a passo
- Responder conforme a intenção da pergunta

⚠️ NÃO acessa YAML
⚠️ NÃO decide busca
"""

from typing import Optional


# =========================================================
# 🔹 INTENÇÕES PARA FLOWS
# =========================================================

FLOW_INTENTS = {
    "como": "steps",
    "passo": "steps",
    "procedimento": "steps",
    "etapas": "steps",
    "fazer": "steps",
}


def detect_flow_intent(question: str) -> Optional[str]:
    if not question:
        return None

    q = question.lower()
    for keyword, intent in FLOW_INTENTS.items():
        if keyword in q:
            return intent

    return None


# =========================================================
# 🔹 RENDERIZAÇÃO
# =========================================================

def render_flow(raw: dict, question: str) -> str:
    title = raw.get("title", "Procedimento")
    description = raw.get("description", "")
    steps = raw.get("steps", [])

    intent = detect_flow_intent(question)

    # -------------------------------
    # 🔹 PASSO A PASSO
    # -------------------------------
    if intent == "steps" and steps:
        lines = [f"🧭 **{title} — Passo a passo**"]
        for idx, step in enumerate(steps, start=1):
            lines.append(f"{idx}. {step}")
        return "\n".join(lines)

    # -------------------------------
    # 🔹 RESUMO
    # -------------------------------
    lines = [f"🧭 **{title}**"]

    if description:
        lines.append(f"\n{description}")

    if steps:
        lines.append("\nℹ️ Pergunte *como fazer* para ver o passo a passo.")

    return "\n".join(lines)
