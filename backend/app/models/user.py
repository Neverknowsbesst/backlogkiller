from pydantic import BaseModel
from typing import List

class User(BaseModel):
    steam_id: str
    biblioteca: List[str]
