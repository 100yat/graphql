import strawberry
from typing import Optional
from pydantic import BaseModel


@strawberry.type
class GraphUser:
    # User()
    _id: Optional[str] = None
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    description: Optional[str] = None
    sign: str
    image: Optional[str] = None
    balance: Optional[str] = None
    contacts: Optional[str] = None


class User(BaseModel):
    _id: Optional[str] = None
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    description: Optional[str] = None
    sign: str
    image: Optional[str] = None
    balance: Optional[str] = None
    contacts: Optional[str] = None
