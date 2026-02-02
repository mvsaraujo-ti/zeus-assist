# app/services/vault_service.py

import yaml
import re
from pathlib import Path
from typing import Optional, List

VAULT_PATH = Path(__file__).resolve().parent.parent / "vault"

# Cache simples em memória
_VAULT_CACHE = {}


def load_vault_file(filename: str) -> dict:
    if filename in _VAULT_CACHE:
        return _VAULT_CACHE[filename]

    file_path = VAULT_PATH / filename

    if not file_path.exists():
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    _VAULT_CACHE[filename] = data
    return data



def normalize_text(text: str) -> List[str]:
    """
    Normaliza texto para busca:
    - lowercase
    - remove pontuação
    - separa em palavras
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()


def search_flows(question: str) -> Optional[dict]:
    """
    Busca o fluxo mais relevante com base em keywords.
    Retorna o flow com maior score.
    """
    data = load_vault_file("flows.yaml")
    flows = data.get("flows", [])

    question_words = normalize_text(question)

    best_match = None
    best_score = 0

    for flow in flows:
        keywords = flow.get("keywords", [])
        score = 0

        for kw in keywords:
            if kw.lower() in question_words:
                score += 1

        if score > best_score:
            best_score = score
            best_match = flow

    return best_match if best_score > 0 else None
