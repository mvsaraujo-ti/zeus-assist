"""
Conversational Service — ZEUS (CUX)

Responsável por:
- Tornar a resposta mais humana e acolhedora
- Manter tom institucional e profissional
- NÃO alterar conteúdo factual
- NÃO decidir respostas

⚠️ Não acessa Vault
⚠️ Não cria informações
⚠️ Não substitui regras
"""

import random

# =========================================================
# 🔹 FRASES CONTROLADAS (SEM ALUCINAÇÃO)
# =========================================================

OPENERS = [
    "Certo!",
    "Vamos lá.",
    "Claro.",
    "Posso te ajudar com isso.",
    "Aqui vai:",
]

CLOSERS = [
    "Se precisar de algo mais, é só me avisar.",
    "Fico à disposição se precisar.",
    "Caso tenha outra dúvida, é só perguntar.",
    "",  # permite não fechar sempre
]


# =========================================================
# 🔹 FUNÇÃO PRINCIPAL
# =========================================================

def apply_conversational_layer(answer: str) -> str:
    """
    Aplica camada conversacional leve ao texto.

    Regras:
    - Não altera o conteúdo
    - Não reescreve regras
    - Apenas envolve o texto com tom humano
    """
    if not answer:
        return answer

    opener = random.choice(OPENERS)
    closer = random.choice(CLOSERS)

    # Montagem cuidadosa
    parts = []

    if opener:
        parts.append(opener)

    parts.append(answer)

    if closer:
        parts.append(closer)

    return "\n\n".join(parts)
