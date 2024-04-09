import strawberry
import motor.motor_asyncio
import decimal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from strawberry.asgi import GraphQL
from typing import List, Optional
from aio_pika import connect_robust, Message, DeliveryMode
import aioredis

from src.models import Tx, User

cli = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)

db = cli.yat
txs = db.tx
users = db.users
asks = db.asks
votes = db.votes

Users = {
    1: User(
        addr="123",
        name="sergeyi",
        cover="coverSergeyi",
        desc="descSergeyi",
        sign="signSergeyi",
    ),
    2: User(
        addr="456", name="Vova", cover="coverVova", desc="descVova", sign="signVova"
    ),
}


@strawberry.experimental.pydantic.type(model=Tx)
class GraphTx:
    credit: Optional[str]
    debit: Optional[str]
    amount: Optional[float]
    time: Optional[decimal.Decimal]
    sign: Optional[str]
    hash: strawberry.auto
    msg: strawberry.auto


@strawberry.type
class GraphUser:
    # User()
    addr: str
    name: Optional[str]
    cover: Optional[str]
    desc: Optional[str]
    sign: str


# @strawberry.type
# class


async def get_balance(addr):
    #ok = await redis.set("key", "value")
    #assert ok
    #b = await redis.get(addr)
    b = 1
    print(int(b), addr)
    return int(b)

async def send_user(addr, name, cover, desc, sign):
    print(addr, name, cover, desc, sign)
    return None

async def get_tx(amount, addr, msg, time, skip, limit) -> List[GraphTx]:
    if amount >= 0: amount_direction = '$gt'
    else: amount_direction = '$lt'; amount = -amount
    
    if time >= 0: time_direction = '$gt'
    else: time_direction = '$lt'; time = -amount

    q = {
        "amount": {amount_direction: amount},
        "time": {time_direction: time},
    }

    if msg != None:
        if msg == True:
            q["msg"] = {"$ne": "null"}
        else:
            q["msg"] = "null"

    if addr:
        q["$or"] = [{"credit": addr}, {"debit": addr}]

    print(q)

    return [
        GraphTx.from_pydantic(Tx(**t))
        for t in await txs.find({"$query": q, "$orderby": {"_id": -1}})
        .skip(skip)
        .limit(limit)
        .to_list(None)
    ]

async def send_tx(tx: Tx) -> str:
    print(jsonable_encoder(tx))
    return "ok"

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
        return await get_tx(amount, addr, msg, time, skip, limit)
    
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
        return await send_tx(amount, addr, msg, time, skip, limit)
    

    @strawberry.field
    async def sendUser(
        self,
        addr: str = "",
        name: str = "",
        cover: str = "",
        desc: str = "",
        sign: str = "",
    ) -> None:
        return await send_user(addr, name, cover, desc, sign)

    @strawberry.field
    async def getBalance(
        self,
        addr: str = ''
    ) -> float:
        return await get_balance(addr)

    @strawberry.field
    def getUser(self, _id: int) -> GraphUser:
        return GraphUser(
            addr="123",
            name="sergeyi",
            cover="coverSergeyi",
            desc="descSergeyi",
            sign="signSergeyi",
        )

    @strawberry.field
    def get_all_user(self) -> list[GraphUser]:
        return [
            GraphUser(
                addr="123",
                name="sergeyi",
                cover="coverSergeyi",
                desc="descSergeyi",
                sign="signSergeyi",
            )
        ]

    @strawberry.field
    def get_all_TX(self) -> list[GraphTx]:
        return [
            GraphTx(
                credit="123",
                debit="321",
                amount=123.456,
                time=1234567890,
                hash="123qwe",
                msg="message qwe123",
                sign="sign что бы это не значило",
            )
        ]

    @strawberry.field
    def get_TX_by_id(self, _id: int) -> GraphTx:
        return GraphTx(
            credit="123",
            debit="321",
            amount=123.456,
            time=1234567890,
            hash="123qwe",
            msg="message qwe123",
            sign="sign что бы это не значило",
        )

    @strawberry.field
    def get_TX_by_user(self, user_id: int) -> GraphTx:
        return GraphTx(
            credit="123",
            debit="321",
            amount=123.456,
            time=1234567890,
            hash="123qwe",
            msg="message qwe123",
            sign="sign что бы это не значило",
        )

    @strawberry.field()
    def get_all_user_contacts(self, user_id: int) -> GraphTx:
        return GraphUser(
            addr="123",
            name="sergeyi",
            cover="coverSergeyi",
            desc="descSergeyi",
            sign="signSergeyi",
        )


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
