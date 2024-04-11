"""атрибут с типом Optional может принимать значение None"""
from typing import Optional
"""BaseModel из библиотеки Pydantiс для создания схемы данных (моделей) 
с автоматической проверкой типов и валидацией данных.
PositiveInt - тип данных - целые положительные числа.
"""
from pydantic import BaseModel, PositiveInt

# Things

class User(BaseModel):
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    sign: str

class Token(BaseModel):
    creater: str
    amount: int
    tiker: str
    img: str
    title: str
    desc: str
    uniq: str
    sign: str
    hash: Optional[str]
    time: Optional[int]

class NFT(BaseModel):
    creater: str
    img: str
    title: str
    desc: str
    uniq: str
    sign: str
    hash: Optional[str]
    time: Optional[int]

class Ask(BaseModel):
    addr: str
    amount: PositiveInt
    uniq: str
    sign: str
    title: Optional[str] = ''
    cover: Optional[str] = ''
    desc: Optional[str] = ''
    hash: Optional[str]
    time: Optional[int]

class Fut(BaseModel):
    creater: str
    amount: PositiveInt
    exp: int
    uniq: str
    sign: str
    hash: Optional[str] #from sign
    time: Optional[int]

class Opt(BaseModel):
    creater: str
    amount: PositiveInt
    exp: int
    uniq: str
    sign: str
    hash: Optional[str] #from sign
    time: Optional[int]


# Actions
class Tx(BaseModel):
    credit: str
    debit: str
    amount: PositiveInt
    uniq: str
    sign: str
    hash: Optional[str]
    msg: Optional[str] = ''
    time: Optional[int]

class Move(BaseModel):
    credit: str
    debit: str
    type: int
    id: str
    uniq: str
    sign: str
    hash: Optional[str]
    time: Optional[int]

class Vote(BaseModel):
    addr: str
    id: str
    like: bool
    uniq: str
    sign: str
    hash: Optional[str]
    time: Optional[int]