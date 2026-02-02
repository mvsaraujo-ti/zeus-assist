# app/config/settings.py

import os


def is_ai_enabled() -> bool:
    """
    Controla se a IA está habilitada via variável de ambiente.
    """
    return os.getenv("ZEUS_AI_ENABLED", "true").lower() == "true"
