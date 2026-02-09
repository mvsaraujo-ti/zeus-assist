# app/services/vault_writer.py

import os
import yaml
from datetime import datetime


BASE_VAULT_PATH = "app/vault"
HISTORY_DIR = ".history"


def write_vault_item(item_type: str, data: dict) -> str:
    """
    Salva um item no Vault com versionamento automático.
    Se o arquivo já existir, move a versão anterior para .history.
    Retorna o caminho do arquivo salvo.
    """

    item_id = data.get("id")
    if not item_id:
        raise ValueError("Campo 'id' é obrigatório para versionamento.")

    folder = _resolve_folder(item_type)
    os.makedirs(folder, exist_ok=True)

    filename = f"{item_id}.yaml"
    file_path = os.path.join(folder, filename)

    # Se já existe, versiona
    if os.path.exists(file_path):
        _archive_previous_version(item_type, item_id, file_path)

    # Salva versão atual
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
        )

    return file_path


# -------------------------
# FUNÇÕES AUXILIARES
# -------------------------

def _resolve_folder(item_type: str) -> str:
    if item_type == "contact":
        return os.path.join(BASE_VAULT_PATH, "contacts")
    if item_type == "system":
        return os.path.join(BASE_VAULT_PATH, "systems")
    if item_type == "flow":
        return os.path.join(BASE_VAULT_PATH, "flows")

    raise ValueError(f"Tipo inválido: {item_type}")


def _archive_previous_version(item_type: str, item_id: str, file_path: str):
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    history_base = os.path.join(
        BASE_VAULT_PATH,
        HISTORY_DIR,
        f"{item_type}s",
        item_id,
    )

    os.makedirs(history_base, exist_ok=True)

    history_file = os.path.join(history_base, f"{timestamp}.yaml")

    os.rename(file_path, history_file)
