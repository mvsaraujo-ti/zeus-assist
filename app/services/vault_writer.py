import yaml
from pathlib import Path
from typing import Literal

from app.schemas.vault.system import SystemSchema
from app.schemas.vault.flow import FlowSchema
from app.schemas.vault.contact import ContactSchema

VAULT_PATH = Path(__file__).resolve().parent.parent / "vault"


def write_vault_item(
    item_type: Literal["system", "flow", "contact"],
    payload: dict,
) -> str:
    """
    Valida payload com Pydantic e salva YAML no vault.

    Retorna o caminho do arquivo criado.
    """

    if item_type == "system":
        obj = SystemSchema(**payload)
        subdir = "systems"

    elif item_type == "flow":
        obj = FlowSchema(**payload)
        subdir = "flows"

    elif item_type == "contact":
        obj = ContactSchema(**payload)
        subdir = "contacts"

    else:
        raise ValueError("Tipo inválido")

    # Garante diretório
    dir_path = VAULT_PATH / subdir
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / f"{obj.id}.yaml"

    # Salva YAML
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            obj.model_dump(),
            f,
            sort_keys=False,
            allow_unicode=True,
        )

    return str(file_path)
