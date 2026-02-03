"""
Guardrails — ZEUS

Responsável por:
- Bloquear perguntas fora do escopo institucional
- Permitir consultas objetivas (lookup), mesmo curtas
- Evitar uso indevido do assistente

⚠️ NÃO decide respostas
⚠️ NÃO interpreta intenção complexa
⚠️ Atua APENAS como filtro inicial
"""

import re


# =========================================================
# 🔹 PALAVRAS FORA DO ESCOPO INSTITUCIONAL
# =========================================================
# ZEUS NÃO responde questões jurídicas nem temas sensíveis

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
# 🔹 PALAVRAS QUE INDICAM CONSULTA DIRETA (LOOKUP)
# =========================================================
# Mesmo perguntas curtas devem ser permitidas se forem lookup

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
}


# =========================================================
# 🔹 FUNÇÃO PRINCIPAL
# =========================================================

def validate_question(question: str) -> None:
    """
    Valida se a pergunta está dentro do escopo do ZEUS.

    Regras aplicadas:
    1. Pergunta deve existir e ser string
    2. Bloqueia termos jurídicos
    3. Permite lookup direto (mesmo sem verbo)
    4. Bloqueia frases muito curtas sem contexto
    """

    # -----------------------------------------------------
    # 1️⃣ VALIDAÇÃO BÁSICA
    # -----------------------------------------------------
    if not question or not isinstance(question, str):
        raise ValueError("Pergunta inválida.")

    text = question.lower().strip()

    # -----------------------------------------------------
    # 2️⃣ BLOQUEIO DE TEMAS FORA DO ESCOPO
    # -----------------------------------------------------
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in text:
            raise ValueError(
                "Questões jurídicas não são respondidas pelo ZEUS. "
                "Por favor, abra um chamado para o setor responsável."
            )

    # -----------------------------------------------------
    # 3️⃣ NORMALIZAÇÃO PARA ANÁLISE SIMPLES
    # -----------------------------------------------------
    words = re.sub(r"[^\w\s]", "", text).split()

    # -----------------------------------------------------
    # 4️⃣ PERMITIR LOOKUP DIRETO
    # -----------------------------------------------------
    # Exemplo:
    # - "telefone da informática"
    # - "email dtic"
    # - "horário do suporte"
    if any(word in LOOKUP_KEYWORDS for word in words):
        return

    # -----------------------------------------------------
    # 5️⃣ BLOQUEAR FRASES MUITO CURTAS E GENÉRICAS
    # -----------------------------------------------------
    # Exemplo:
    # - "oi"
    # - "ajuda"
    # - "suporte"
    if len(words) < 3:
        raise ValueError(
            "Por favor, informe um pouco mais de contexto para que eu possa ajudar."
        )

    # -----------------------------------------------------
    # 6️⃣ PERMITIR PERGUNTA
    # -----------------------------------------------------
    return
