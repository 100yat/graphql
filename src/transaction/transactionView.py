import motor.motor_asyncio
import strawberry
from typing import List
from src.transaction.transactionModel import GraphTx, Tx
from src.transaction.transactionController import TransactionController

cli = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)

db = cli.yat
txs = db.tx
tx_controller = TransactionController(db)


@strawberry.type
class TransactionQuery:
    @strawberry.field
    async def getTx(
        self,
        msg: bool = None,
        addr: str = "",
        amount: int = 0,
        time: int = 0,
        skip: int = 0,
        limit: int = 100,
    ) -> List[GraphTx]:
        return tx_controller.get_tx(amount, addr, msg, time, skip, limit)

    @strawberry.field
    async def sendTx(
        self,
        addr: str,
        amount: int,
        fromUserId: str,
        toUserId: str,
        msg: str = None,
        time: int = 0,
        skip: int = 0,
        limit: int = 100,
    ) -> GraphTx:
        tx = Tx(amount=amount,
                addr=addr,
                msg=msg,
                time=time,
                skip=skip,
                limit=limit,
                fromUserId=fromUserId,
                toUserId=toUserId)
        return await tx_controller.send_tx(tx)

    @strawberry.field
    def get_all_TX(self) -> list[GraphTx]:
        return tx_controller.get_all_TX()

    @strawberry.field
    def get_TX_by_id(self, _id: int) -> GraphTx:
        return tx_controller.get_TX_by_id()

    @strawberry.field
    def get_TX_by_user(self, user_id: int) -> GraphTx:
        return tx_controller.get_TX_by_user(user_id)


schema = strawberry.Schema(query=TransactionQuery) # кажется это должно быть здесь
