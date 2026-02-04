from pydantic import BaseModel
from typing import List, Optional, Literal


class FlowSchema(BaseModel):
    type: Literal["flow"] = "flow"
    id: str
    title: str
    keywords: List[str]

    description: Optional[str] = None
    steps: List[str]
