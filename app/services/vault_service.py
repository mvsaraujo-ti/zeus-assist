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
# Reinício do backend limpa o cache
_VAULT_CACHE: Dict[str, dict] = {}


# =========================================================
# 🔹 LOADERS (LEITURA DE YAML)
# =========================================================

def load_vault_file(filename: str) -> dict:
    """
    Carrega arquivo YAML do vault com cache em memória.

    - Usa yaml.safe_load (segurança)
    - Nunca lança exceção
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


# =========================================================
# 🔹 NORMALIZAÇÃO DE TEXTO
# =========================================================

def normalize_text(text: str) -> List[str]:
    """
    Normaliza texto para busca previsível.

    Exemplo:
    "Solicitação de Acesso ao DigiDoc!" →
    ["solicitação", "de", "acesso", "ao", "digidoc"]
    """
    if not text:
        return []

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()


# =========================================================
# 🔹 NORMALIZAÇÃO DOS DADOS DO VAULT
# =========================================================

def normalize_flows(flows: list) -> list:
    """
    Normaliza flows.yaml para o formato interno padrão.
    """
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
    """
    Normaliza systems.yaml para o formato interno padrão.
    """
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
    """
    Normaliza contacts.yaml para o formato interno padrão.
    """
    items = []

    for contact in contacts:
        items.append({
            "type": "contact",
            "id": contact.get("id"),
            "title": contact.get("sector", ""),
            "keywords": contact.get("keywords", []),
            "content": contact.get("notes", ""),
            "raw": contact
        })

    return items


# =========================================================
# 🔹 SCORER (FUNÇÃO DE PONTUAÇÃO)
# =========================================================

def score_item(question_words: List[str], item: dict) -> int:
    """
    Calcula score de relevância entre pergunta e item.

    Pesos:
    - Título: peso 3
    - Keywords: peso 2
    - Conteúdo: peso 1
    """
    score = 0

    # Peso alto para título
    title_words = normalize_text(item.get("title", ""))
    for word in title_words:
        if word in question_words:
            score += 3

    # Peso médio para keywords
    for kw in item.get("keywords", []):
        if kw.lower() in question_words:
            score += 2

    # Peso leve para conteúdo
    content_words = normalize_text(item.get("content", ""))
    for word in content_words:
        if word in question_words:
            score += 1

    return score


# =========================================================
# 🔹 BUSCA UNIFICADA
# =========================================================

def search(question: str) -> Optional[dict]:
    """
    Executa busca unificada no vault.

    Fluxo:
    1. Normaliza pergunta
    2. Detecta intenção explícita (ex: contato)
    3. Carrega YAMLs
    4. Normaliza dados
    5. Aplica score
    6. Retorna melhor item
    """
    question_words = normalize_text(question)

    # -----------------------------------------------------
    # 🔹 DETECÇÃO DE INTENÇÃO DE CONTATO
    # -----------------------------------------------------
    contact_intent_words = {
        "telefone",
        "fone",
        "email",
        "e-mail",
        "horario",
        "horário",
        "contato",
    }

    is_contact_intent = any(
        word in question_words for word in contact_intent_words
    )

    # -----------------------------------------------------
    # 🔹 CARREGA DADOS DO VAULT
    # -----------------------------------------------------
    flows = load_vault_file("flows.yaml").get("flows", [])
    systems = load_vault_file("systems.yaml").get("systems", [])
    contacts = load_vault_file("contacts.yaml").get("contacts", [])

    # -----------------------------------------------------
    # 🔹 SELEÇÃO DE ITENS CONFORME INTENÇÃO
    # -----------------------------------------------------
    if is_contact_intent:
        # Intenção clara → prioriza contatos
        items = normalize_contacts(contacts)
    else:
        # Busca geral
        items = (
            normalize_flows(flows)
            + normalize_systems(systems)
            + normalize_contacts(contacts)
        )

    # -----------------------------------------------------
    # 🔹 APLICA SCORE
    # -----------------------------------------------------
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
