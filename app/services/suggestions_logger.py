"""
Suggestions Logger — ZEUS

Responsável por:
- Registrar eventos de fallback e sugestão
- Gerar observabilidade leve
- Apoiar evolução do Vault (YAML)

⚠️ Append-only (JSON Lines)
⚠️ Sem banco
⚠️ Sem IA
⚠️ Auditável
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from app.services.vault_service import normalize_text


# =========================================================
# 🔹 CONFIGURAÇÃO DO LOG
# =========================================================

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "suggestions_log.jsonl"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


# =========================================================
# 🔹 API DE LOG
# =========================================================

def log_suggestion(
    query: str,
    suggestions: List[str],
    intent: str = "suggestion",
    reason: Optional[str] = None,
) -> None:
    """
    Registra um evento de sugestão ou fallback.

    Cada chamada gera uma linha JSON independente.
    """

    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "normalized_query": normalize_text(query),
        "intent": intent,
        "reason": reason,
        "suggestions": suggestions,
    }

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
