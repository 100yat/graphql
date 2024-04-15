from pydantic import BaseModel, PositiveInt
import strawberry
from typing import Optional
import decimal


class Tx(BaseModel):
    credit: str
    debit: str
    amount: PositiveInt
    uniq: str
    sign: str
    hash: Optional[str]
    msg: Optional[str] = ''
    time: Optional[int]


@strawberry.experimental.pydantic.type(model=Tx)
class GraphTx:
    credit: Optional[str]
    debit: Optional[str]
    amount: Optional[float]
    time: Optional[decimal.Decimal]
    sign: Optional[str]
    hash: strawberry.auto
    msg: strawberry.auto
