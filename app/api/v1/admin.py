# app/api/v1/admin.py

from fastapi import APIRouter, HTTPException
from typing import Literal

from app.services.vault_writer import write_vault_item
from app.core.vault_validator import validate

router = APIRouter(tags=["Admin"])


@router.post("/vault/{item_type}")
def create_vault_item(
    item_type: Literal["system", "flow", "contact"],
    payload: dict,
):
    errors = validate(item_type, payload)

    if errors:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Erro de validação do Vault",
                "errors": errors,
            },
        )

    try:
        path = write_vault_item(item_type, payload)
        return {
            "status": "ok",
            "path": path,
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
