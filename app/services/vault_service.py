"""
Vault Service — ZEUS

Responsável por:
- Ler arquivos YAML do vault (único ponto autorizado)
- Normalizar dados institucionais
- Executar busca unificada e previsível
- Respeitar prioridade por intenção
- Retornar item OU sugestões (sem decidir resposta)

⚠️ IA NÃO entra aqui
⚠️ YAML continua sendo a fonte da verdade
"""

import yaml
import re
import unicodedata
from pathlib import Path
from typing import Optional, List, Dict

from app.core.synonyms import SYNONYMS_MAP

# =========================================================
# CONFIGURAÇÃO BASE
# =========================================================

VAULT_PATH = Path(__file__).resolve().parent.parent / "vault"
_VAULT_CACHE: Dict[str, dict] = {}

# =========================================================
# LOADERS
# =========================================================

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


def load_vault_dir(subdir: str) -> List[dict]:
    items = []
    dir_path = VAULT_PATH / subdir

    if not dir_path.exists():
        return items

    for file in dir_path.glob("*.yaml"):
        data = load_vault_file(f"{subdir}/{file.name}")
        if data:
            items.append(data)

    return items


# =========================================================
# NORMALIZAÇÃO
# =========================================================

def normalize_text(text: str) -> List[str]:
    if not text:
        return []

    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^\w\s]", "", text)

    return text.split()


def expand_with_synonyms(words: List[str]) -> List[str]:
    expanded = set(words)

    for word in words:
        for base, synonyms in SYNONYMS_MAP.items():
            if word == base or word in synonyms:
                expanded.add(base)
                expanded.update(synonyms)

    return list(expanded)


# =========================================================
# NORMALIZAÇÃO DOS ITENS
# =========================================================

def normalize_items(items: list, item_type: str) -> list:
    return [
        {
            "type": item_type,
            "id": item.get("id"),
            "title": item.get("name") or item.get("title", ""),
            "keywords": item.get("keywords", []),
            "content": item.get("description", ""),
            "raw": item,
        }
        for item in items
    ]


# =========================================================
# MATCHES FORTES (ANTI FALSE-POSITIVE)
# =========================================================

def has_strong_match(question_words: List[str], item: dict) -> bool:
    """
    SYSTEM e FLOW só são válidos se houver match explícito
    no title OU keywords.
    """

    # Match no title (identificador principal)
    title_words = normalize_text(item.get("title", ""))
    if any(word in question_words for word in title_words):
        return True

    # Match em keywords
    for kw in item.get("keywords", []):
        kw_words = normalize_text(kw)
        if any(word in question_words for word in kw_words):
            return True

    return False


# =========================================================
# SCORER (RANKING SECUNDÁRIO)
# =========================================================

def score_item(question_words: List[str], item: dict) -> int:
    score = 0

    # Title: peso alto
    for word in normalize_text(item.get("title", "")):
        if word in question_words:
            score += 3

    # Keywords: peso médio
    for kw in item.get("keywords", []):
        for word in normalize_text(kw):
            if word in question_words:
                score += 2

    # Content: peso baixo (NUNCA decisivo para SYSTEM/FLOW)
    for word in normalize_text(item.get("content", "")):
        if word in question_words:
            score += 1

    return score


# =========================================================
# BUSCA UNIFICADA (COM GOVERNANÇA RÍGIDA)
# =========================================================

def search(question: str) -> Optional[dict]:
    base_words = normalize_text(question)
    expanded_words = expand_with_synonyms(base_words)

    # ----------------------------
    # Intenção explícita de contato
    # ----------------------------
    contact_intent_words = {
        "telefone",
        "fone",
        "email",
        "ramal",
        "contato",
        "horario",
    }

    is_contact_intent = any(word in expanded_words for word in contact_intent_words)

    # ----------------------------
    # Carrega dados
    # ----------------------------
    contacts = normalize_items(load_vault_dir("contacts"), "contact")
    systems = normalize_items(load_vault_dir("systems"), "system")
    flows = normalize_items(load_vault_dir("flows"), "flow")

    # ----------------------------
    # PRIORIDADE ABSOLUTA: CONTACT
    # ----------------------------
    if is_contact_intent:
        best_contact = None
        best_score = 0
        suggestions = set()

        for item in contacts:
            score = score_item(expanded_words, item)
            suggestions.update(item.get("keywords", []))

            if score > best_score:
                best_score = score
                best_contact = item

        if best_contact and best_score > 0:
            best_contact["score"] = best_score
            return best_contact

        return {
            "type": "suggestion",
            "intent": "contact",
            "suggestions": sorted(suggestions),
        }

    # ----------------------------
    # BUSCA NORMAL (FLOW + SYSTEM + CONTACT)
    # ----------------------------
    items = flows + systems + contacts

    best_item = None
    best_score = 0
    suggestions = set()

    for item in items:
        # 🔒 TRAVA CRÍTICA:
        # SYSTEM e FLOW exigem match forte
        if item["type"] in {"system", "flow"}:
            if not has_strong_match(expanded_words, item):
                continue

        score = score_item(expanded_words, item)
        suggestions.update(item.get("keywords", []))

        if score > best_score:
            best_score = score
            best_item = item

    if best_item and best_score > 0:
        best_item["score"] = best_score
        return best_item

    # ----------------------------
    # FALLBACK COM SUGESTÃO
    # ----------------------------
    return {
        "type": "suggestion",
        "intent": "generic",
        "suggestions": sorted(suggestions),
    }
