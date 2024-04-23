import strawberry
from src.balance.balanceController import BalanceController


@strawberry.type
class BalanceQuery:

    @strawberry.field
    async def getBalance(self, addr: str = "") -> float:
        return BalanceController().get_balance(addr)
