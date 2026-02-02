# app/core/guardrails.py

def validate_question(question: str) -> None:
    """
    Aplica regras básicas antes de processar a pergunta.

    Regras:
    - ZEUS não responde questões jurídicas
    """
    forbidden_keywords = [
        "lei",
        "artigo",
        "processo judicial",
        "jurídico",
        "sentença",
    ]

    question_lower = question.lower()

    for keyword in forbidden_keywords:
        if keyword in question_lower:
            raise ValueError(
                "Questões jurídicas não são respondidas pelo ZEUS. "
                "Por favor, abra um chamado."
            )
