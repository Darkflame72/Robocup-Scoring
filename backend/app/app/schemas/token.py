from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[UUID4] = None
