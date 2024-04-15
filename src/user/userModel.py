import strawberry
from typing import Optional
from pydantic import BaseModel


@strawberry.type
class GraphUser:
    # User()
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    sign: str


class User(BaseModel):
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    sign: str
