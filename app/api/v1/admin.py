from fastapi import APIRouter, HTTPException, Depends
from typing import Literal

from app.services.vault_writer import write_vault_item
from app.core.admin_auth import admin_auth

router = APIRouter(tags=["Admin"])


@router.post("/vault/{item_type}")
def create_vault_item(
    item_type: Literal["system", "flow", "contact"],
    payload: dict,
    user: str = Depends(admin_auth),
):
    try:
        path = write_vault_item(item_type, payload)
        return {
            "status": "ok",
            "user": user,
            "path": path,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
