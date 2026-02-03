"""
Conversational Service (CUX) — ZEUS

Responsável por:
- Humanizar respostas institucionais
- Melhorar tom e acolhimento
- Manter conforto conversacional

⚠️ NÃO decide conteúdo
⚠️ NÃO acessa YAML
⚠️ NÃO altera fatos
⚠️ NÃO substitui regras
"""

from app.services.ai_service import enhance_answer


# =========================================================
# 🔹 FRASES INSTITUCIONAIS PADRÃO
# =========================================================

OPENING_PHRASES = [
    "Claro, posso te ajudar com isso.",
    "Sem problema, veja a informação abaixo.",
    "Aqui está a informação que você solicitou.",
]

CLOSING_PHRASES = [
    "Se precisar de mais alguma coisa, é só me dizer.",
    "Fico à disposição caso precise de mais ajuda.",
    "Se quiser, posso te orientar sobre o próximo passo.",
]


# =========================================================
# 🔹 FUNÇÃO PRINCIPAL
# =========================================================

def apply_conversational_layer(
    answer: str,
    *,
    add_opening: bool = True,
    add_closing: bool = True,
    use_ai: bool = True
) -> str:
    """
    Aplica camada conversacional controlada à resposta.

    Parâmetros:
    - answer: texto institucional já pronto
    - add_opening: adiciona frase de abertura
    - add_closing: adiciona frase de encerramento
    - use_ai: permite IA apenas para TOM

    Retorna:
    - Texto mais humano, sem alterar conteúdo
    """

    if not answer or not isinstance(answer, str):
        return answer

    parts = []

    # -----------------------------------------------------
    # 1️⃣ Abertura institucional (opcional)
    # -----------------------------------------------------
    if add_opening:
        parts.append(OPENING_PHRASES[0])

    # -----------------------------------------------------
    # 2️⃣ Conteúdo principal (determinístico)
    # -----------------------------------------------------
    parts.append(answer)

    # -----------------------------------------------------
    # 3️⃣ Encerramento gentil (opcional)
    # -----------------------------------------------------
    if add_closing:
        parts.append(CLOSING_PHRASES[0])

    final_text = "\n\n".join(parts)

    # -----------------------------------------------------
    # 4️⃣ IA apenas para TOM (opcional)
    # -----------------------------------------------------
    if use_ai:
        final_text = enhance_answer(final_text)

    return final_text
