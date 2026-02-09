# app/core/synonyms.py

"""
Sinônimos controlados do ZEUS.

⚠️ Não é correção ortográfica
⚠️ Não é fuzzy search
⚠️ Não é IA

Objetivo:
- Mapear termos comuns do usuário para termos institucionais
"""

SYNONYMS_MAP = {
    # Informática / TI
    "informatica": ["ti", "tecnologia", "suporte", "informática"],
    "ti": ["informatica", "informática", "tecnologia"],
    "suporte": ["ti", "informatica", "informática"],

    # Senha
    "senha": ["password", "acesso", "login"],

    # Sistema
    "sistema": ["aplicacao", "aplicação", "portal"],

    # Contato
    "telefone": ["fone", "contato", "ramal"],
    "email": ["e-mail", "correio"],

    # Horário
    "horario": ["horário", "expediente"],
}
