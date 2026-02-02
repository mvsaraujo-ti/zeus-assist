# app/services/ai_service.py

from app.providers.ollama_client import format_answer_with_ollama
from app.config.settings import is_ai_enabled


def enhance_answer(answer: str) -> str:
    """
    Usa IA apenas se:
    - estiver habilitada
    - o texto for suficientemente grande
    """

    if not is_ai_enabled():
        return answer

    # Regra simples: texto curto já é bom
    if len(answer) < 300:
        return answer

    return format_answer_with_ollama(answer)
