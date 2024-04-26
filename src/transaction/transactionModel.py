from pydantic import BaseModel, PositiveInt
import strawberry
from typing import Optional
import decimal


class Tx(BaseModel):
    Id: Optional[str] = None
    addr: Optional[str] = None
    credit: str = None
    debit: str = None
    amount: Optional[PositiveInt] = None
    uniq: str = None
    sign: str = None
    hash: Optional[str] = None
    msg: Optional[str] = None
    time: Optional[int] = None
    fromUserId: Optional[str] = None
    toUserId: Optional[str] = None


@strawberry.experimental.pydantic.type(model=Tx)
class GraphTx:
    Id: Optional[str] = None
    addr: Optional[str] = None
    credit: Optional[str] = None
    debit: Optional[str] = None
    amount: Optional[float] = None
    time: Optional[decimal.Decimal] = None
    sign: Optional[str] = None
    uniq: str = None
    hash: strawberry.auto = None
    msg: strawberry.auto = None
    fromUserId: Optional[str] = None
    toUserId: Optional[str] = None
