from pydantic import BaseModel, PositiveInt
import strawberry
from typing import Optional
import decimal


class Balance(BaseModel):
    Id: Optional[str] = None
    UserId: Optional[str] = None
    addr: Optional[str] = None
    amount: Optional[float] = None


@strawberry.experimental.pydantic.type(model=Balance)
class GraphBalance:
    Id: Optional[str] = None
    UserId: Optional[str] = None
    addr: Optional[str] = None
    amount: Optional[float] = None
