# app/core/vault_validator.py

from typing import List


def validate(item_type: str, data: dict) -> List[str]:
    """
    Valida semanticamente um item do Vault.
    Retorna lista de erros. Lista vazia = válido.
    """
    errors: List[str] = []

    if not isinstance(data, dict):
        return ["Payload inválido: esperado um objeto JSON."]

    if item_type == "contact":
        errors.extend(_validate_contact(data))

    elif item_type == "system":
        errors.extend(_validate_system(data))

    elif item_type == "flow":
        errors.extend(_validate_flow(data))

    else:
        errors.append(f"Tipo de item inválido: {item_type}")

    return errors


# -------------------------
# VALIDADORES ESPECÍFICOS
# -------------------------

def _validate_contact(data: dict) -> List[str]:
    errors = []

    name = data.get("name")
    keywords = data.get("keywords")
    channels = data.get("channels", {})

    if not name:
        errors.append("Contact: campo 'name' é obrigatório.")

    if not isinstance(keywords, list) or not keywords:
        errors.append("Contact: campo 'keywords' deve ser uma lista não vazia.")

    if not isinstance(channels, dict):
        errors.append("Contact: campo 'channels' deve ser um objeto.")
        return errors

    has_channel = any(
        channels.get(field)
        for field in ("email", "phone", "ramal")
    )

    if not has_channel:
        errors.append(
            "Contact: deve possuir ao menos um canal de contato "
            "(email, phone ou ramal)."
        )

    return errors


def _validate_system(data: dict) -> List[str]:
    errors = []

    description = data.get("description")

    if not description:
        errors.append("System: campo 'description' é obrigatório.")
    elif not isinstance(description, str):
        errors.append("System: campo 'description' deve ser texto.")
    elif len(description.strip()) < 40:
        errors.append(
            "System: 'description' deve ter pelo menos 40 caracteres "
            "para resposta institucional adequada."
        )

    return errors


def _validate_flow(data: dict) -> List[str]:
    errors = []

    title = data.get("title")
    steps = data.get("steps")

    if not title:
        errors.append("Flow: campo 'title' é obrigatório.")

    if steps is not None:
        if not isinstance(steps, list):
            errors.append("Flow: campo 'steps' deve ser uma lista.")
        elif len(steps) < 2:
            errors.append(
                "Flow: campo 'steps' deve conter pelo menos 2 etapas."
            )

    return errors
