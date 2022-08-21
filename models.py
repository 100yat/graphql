from typing import Optional
from pydantic import BaseModel, PositiveInt
import decimal

class Tx(BaseModel):
    credit: str
    debit: str
    amount: PositiveInt
    time: int
    sign: str
    hash: Optional[str]
    msg: Optional[str] = ''
    #type

class UserContent(BaseModel):
    addr: str
    req: str
    time: int
    content: str
    sign: str

class User(BaseModel):
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]