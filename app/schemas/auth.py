# schemas/auth.py
from pydantic import BaseModel
from typing import Dict, List

class AuthResponseWithMeta(BaseModel):
    access_token: str
    token_type: str = "bearer"

