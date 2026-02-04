from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Usuários fixos (depois pode ir para DB)
USERS = {
    "admin": "admin123"
}

def admin_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = USERS.get(credentials.username)

    if not correct_password or not secrets.compare_digest(
        credentials.password,
        correct_password
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return credentials.username
