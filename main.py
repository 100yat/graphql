import strawberry
import motor.motor_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL
from typing import List, Optional
from aio_pika import connect_robust, Message, DeliveryMode
import aioredis
from services import userService, txService, balanceService
from src.graphqlModels import GraphTx, GraphUser

cli = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)

db = cli.yat
txs = db.tx
users = db.users
asks = db.asks
votes = db.votes

user = userService.UserService()
tx = txService.Tx(txs)
balance = balanceService.BalanceService()


@strawberry.type
class Query:
    @strawberry.field
    async def getTx(
        self,
        msg: bool = None,
        addr: str = '',
        amount: int = 0,
        time: int = 0,
        skip: int = 0,
        limit: int = 100
    ) -> List[GraphTx]:
        return tx.get_tx(amount, addr, msg, time, skip, limit)
    
    @strawberry.field
    async def sendTx(
        self,
        msg: bool = None,
        addr: str = "",
        amount: int = 0,
        time: int = 0,
        skip: int = 0,
        limit: int = 100,
    ) -> List[GraphTx]:
        return tx.send_tx(amount, addr, msg, time, skip, limit)
    

    @strawberry.field
    async def sendUser(
        self,
        addr: str = "",
        name: str = "",
        cover: str = "",
        desc: str = "",
        sign: str = "",
    ) -> None:
        return user.send_user(addr, name, cover, desc, sign)

    @strawberry.field
    async def getBalance(
        self,
        addr: str = ''
    ) -> float:
        return balance.get_balance(addr)

    @strawberry.field
    def getUser(self, _id: int) -> GraphUser:
        return user.get_user()

    @strawberry.field
    def get_all_user(self) -> list[GraphUser]:
        return user.get_all_user()

    @strawberry.field
    def get_all_TX(self) -> list[GraphTx]:
        return tx.get_all_TX()

    @strawberry.field
    def get_TX_by_id(self, _id: int) -> GraphTx:
        return tx.get_TX_by_id()

    @strawberry.field
    def get_TX_by_user(self, user_id: int) -> GraphTx:
        return tx.get_TX_by_user(user_id)

    @strawberry.field()
    def get_all_user_contacts(self, user_id: int) -> GraphTx:
        return user.get_all_user_contacts(user_id)


schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)  # graphiql=False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    global mq
    connection = await connect_robust("amqp://guest:guest@localhost/")
    mq = await connection.channel()
    queue = await mq.declare_queue("tx", durable=True)
    global redis
    redis = await aioredis.from_url("redis://localhost", db=0)


app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
