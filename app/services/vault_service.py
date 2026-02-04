"""
Vault Service — ZEUS

Responsável por:
- Ler arquivos YAML do vault (único ponto autorizado)
- Normalizar dados institucionais
- Executar busca unificada e previsível
- Retornar o item mais relevante (sem decidir resposta)

⚠️ IA NÃO entra aqui
⚠️ YAML continua sendo a fonte da verdade
"""

import yaml
import re
from pathlib import Path
from typing import Optional, List, Dict

# =========================================================
# 🔹 CONFIGURAÇÃO BASE
# =========================================================

VAULT_PATH = Path(__file__).resolve().parent.parent / "vault"

# Cache simples em memória
_VAULT_CACHE: Dict[str, dict] = {}


# =========================================================
# 🔹 LOADERS
# =========================================================

def load_vault_file(filename: str) -> dict:
    """
    Carrega um arquivo YAML do vault com cache.
    """
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
    """
    Carrega todos os arquivos YAML de um diretório do vault.
    """
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
# 🔹 NORMALIZAÇÃO DE TEXTO
# =========================================================

def normalize_text(text: str) -> List[str]:
    if not text:
        return []

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()


# =========================================================
# 🔹 NORMALIZAÇÃO DOS ITENS
# =========================================================

def normalize_flows(flows: list) -> list:
    items = []

    for flow in flows:
        items.append({
            "type": "flow",
            "id": flow.get("id"),
            "title": flow.get("title", ""),
            "keywords": flow.get("keywords", []),
            "content": flow.get("description", ""),
            "raw": flow
        })

    return items


def normalize_systems(systems: list) -> list:
    items = []

    for system in systems:
        items.append({
            "type": "system",
            "id": system.get("id"),
            "title": system.get("name", ""),
            "keywords": system.get("keywords", []),
            "content": system.get("description", ""),
            "raw": system
        })

    return items


def normalize_contacts(contacts: list) -> list:
    items = []

    for contact in contacts:
        items.append({
            "type": "contact",
            "id": contact.get("id"),
            "title": contact.get("name", ""),
            "keywords": contact.get("keywords", []),
            "content": "",
            "raw": contact
        })

    return items


# =========================================================
# 🔹 SCORER
# =========================================================

def score_item(question_words: List[str], item: dict) -> int:
    score = 0

    # Título (peso 3)
    for word in normalize_text(item.get("title", "")):
        if word in question_words:
            score += 3

    # Keywords (peso 2)
    for kw in item.get("keywords", []):
        if kw.lower() in question_words:
            score += 2

    # Conteúdo (peso 1)
    for word in normalize_text(item.get("content", "")):
        if word in question_words:
            score += 1

    return score


# =========================================================
# 🔹 BUSCA UNIFICADA
# =========================================================

def search(question: str) -> Optional[dict]:
    question_words = normalize_text(question)

    # ----------------------------
    # Intenção explícita de contato
    # ----------------------------
    contact_intent_words = {
        "telefone",
        "fone",
        "email",
        "e-mail",
        "ramal",
        "contato",
        "horario",
        "horário",
    }

    is_contact_intent = any(
        word in question_words for word in contact_intent_words
    )

    # ----------------------------
    # Carrega dados do vault
    # ----------------------------
    flows = load_vault_dir("flows")
    systems = load_vault_dir("systems")
    contacts = load_vault_dir("contacts")

    # ----------------------------
    # Seleção conforme intenção
    # ----------------------------
    if is_contact_intent:
        items = normalize_contacts(contacts)
    else:
        items = (
            normalize_systems(systems)
            + normalize_flows(flows)
            + normalize_contacts(contacts)
        )

    # ----------------------------
    # Scoring
    # ----------------------------
    best_item = None
    best_score = 0

    for item in items:
        score = score_item(question_words, item)
        if score > best_score:
            best_score = score
            best_item = item

    if best_item and best_score > 0:
        best_item["score"] = best_score
        return best_item

    return None
