import strawberry
from typing import Optional, List
from src import models
import decimal

@strawberry.type
class GraphUser:
    # User()
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    sign: str

@strawberry.experimental.pydantic.type(model=models.Tx)
class GraphTx:
    credit: Optional[str]
    debit: Optional[str]
    amount: Optional[float]
    time: Optional[decimal.Decimal]
    sign: Optional[str]
    hash: strawberry.auto
    msg: strawberry.auto