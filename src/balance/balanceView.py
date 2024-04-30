import motor.motor_asyncio
import strawberry
from typing import List
from src.balance.balanceModel import GraphBalance, Balance
from src.balance.balanceController import BalanceController

cli = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)

db = cli.yat
txs = db.tx
users = db.users
balance_controller = BalanceController(db)


@strawberry.type
class BalanceQuery:
    @strawberry.field
    async def getBalance(
        self,
        addr: str = "",
        amount: int = 0,
    ) -> GraphBalance:
        return balance_controller.get_balance(addr)
    
    @strawberry.field
    def get_all_Balances(self) -> List[GraphBalance]:
        return balance_controller.get_all_Balances()
    
    @strawberry.field
    def get_balance_by_user(self, user_id: int) -> GraphBalance:
        return balance_controller.get_balance_by_user(user_id)


schema = strawberry.Schema(query=BalanceQuery)
