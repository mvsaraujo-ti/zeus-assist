from pydantic import BaseModel
from typing import List, Optional, Literal


class ContactChannels(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    ramal: Optional[str] = None


class ContactSchema(BaseModel):
    type: Literal["contact"] = "contact"
    id: str
    name: str
    keywords: List[str]

    channels: ContactChannels
    hours: Optional[str] = None
