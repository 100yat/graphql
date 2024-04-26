import strawberry
from typing import Optional
from pydantic import BaseModel
from src.transaction.transactionModel import Tx, GraphTx


@strawberry.type
class GraphUser:
    # User()
    Id: Optional[str] = None
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    description: Optional[str] = None
    sign: str
    image: Optional[str] = None
    balance: Optional[int] = 0
    contacts: Optional[str] = None


class User(BaseModel):
    Id: Optional[str] = None
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    description: Optional[str] = None
    sign: str
    image: Optional[str] = None
    balance: Optional[int] = 0
    contacts: Optional[str] = None
