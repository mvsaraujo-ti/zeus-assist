"""
AI Service

Responsável exclusivamente por:
- Melhorar a FORMA do texto (clareza, organização, tom)
- Nunca decidir conteúdo
- Nunca acessar YAML
- Nunca ser ponto crítico do sistema

⚠️ Se a IA falhar, o ZEUS continua funcionando normalmente.
"""

from app.providers.ollama_client import format_answer_with_ollama
from app.config.settings import is_ai_enabled

# =========================================================
# 🔹 CONFIGURAÇÕES INTERNAS
# =========================================================

# Tamanho mínimo do texto para justificar uso de IA
# Textos curtos já são suficientemente legíveis
MIN_TEXT_LENGTH_FOR_AI = 300

# Tamanho máximo de texto enviado para IA
# Evita custo alto, lentidão e problemas de contexto
MAX_TEXT_LENGTH_FOR_AI = 3000


# =========================================================
# 🔹 FUNÇÃO PÚBLICA
# =========================================================

def enhance_answer(answer: str) -> str:
    """
    Aplica melhoria de formatação via IA, se habilitada.

    Regras de segurança:
    - IA é opcional (feature flag)
    - Texto curto não passa pela IA
    - Texto muito grande é truncado
    - Qualquer erro retorna o texto original

    ⚠️ Essa função NUNCA pode lançar exceção.
    """

    # -----------------------------------------------------
    # 1️⃣ Feature flag global
    # -----------------------------------------------------
    if not is_ai_enabled():
        return answer

    # -----------------------------------------------------
    # 2️⃣ Validação defensiva
    # -----------------------------------------------------
    if not answer or not isinstance(answer, str):
        return answer

    text_length = len(answer)

    # -----------------------------------------------------
    # 3️⃣ Texto pequeno não precisa de IA
    # -----------------------------------------------------
    if text_length < MIN_TEXT_LENGTH_FOR_AI:
        return answer

    # -----------------------------------------------------
    # 4️⃣ Truncamento seguro (proteção)
    # -----------------------------------------------------
    safe_answer = answer
    if text_length > MAX_TEXT_LENGTH_FOR_AI:
        safe_answer = answer[:MAX_TEXT_LENGTH_FOR_AI]

    # -----------------------------------------------------
    # 5️⃣ Chamada da IA com fail-safe TOTAL
    # -----------------------------------------------------
    try:
        improved_text = format_answer_with_ollama(safe_answer)

        # Validação da resposta da IA
        if not improved_text or not isinstance(improved_text, str):
            return answer

        return improved_text

    except Exception:
        # ⚠️ Qualquer falha da IA NÃO pode afetar o ZEUS
        return answer
