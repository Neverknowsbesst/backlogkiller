from pydantic import BaseModel
from typing import List

class Game(BaseModel):
    id: str
    nombre: str
    tags: List[str]
