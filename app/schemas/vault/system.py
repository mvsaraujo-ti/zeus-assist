from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Literal


class SystemAccess(BaseModel):
    url: HttpUrl
    login_required: bool = True


class SystemSupport(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None


class SystemSchema(BaseModel):
    type: Literal["system"] = "system"
    id: str
    name: str
    keywords: List[str]

    description: Optional[str] = None
    access: Optional[SystemAccess] = None
    support: Optional[SystemSupport] = None
