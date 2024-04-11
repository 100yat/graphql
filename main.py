"""библиотека Strawberry для создания GraphQL API"""
import strawberry
"""асинхронный драйвер MongoDB для работы с БД"""
import motor.motor_asyncio
""""модуль decimal для работы с десятичными числами"""
import decimal
from fastapi import FastAPI
"""CORS Middleware для обработки CORS-запросов"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
"""модуль GraphQL из библиотеки Strawberry"""
from strawberry.asgi import GraphQL
"""типы данных List и Optional для аннотации типов"""
from typing import List, Optional
"""библиотека aio-pika для работы с RabbitMQ"""
from aio_pika import connect_robust, Message, DeliveryMode
"""библиотека aioredis для работы с Redis"""
import aioredis

"""модели Tx и User из файла src/models.py"""
from src.models import Tx, User

"""Подключение к MongoDB"""
cli = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

"""Выбор базы данных "yat" в MongoDB и определение коллекций"""
db = cli.yat
txs = db.tx
users = db.users
asks = db.asks
votes = db.votes

"""Определение типа GraphTx с использованием аннотаций 
Pydantic и Strawberry для работы с транзакциями"""
@strawberry.experimental.pydantic.type(model=Tx)
class GraphTx:
    credit: Optional[str]
    debit: Optional[str]
    amount: Optional[float]
    time: Optional[decimal.Decimal]
    sign: Optional[str]
    hash: strawberry.auto
    msg: strawberry.auto

"""Определение типа GraphUser с использованием аннотаций 
Pydantic и Strawberry для работы с пользователями"""
@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class GraphUser:
    ...

"""Асинхронная функция для загрузки баланса пользователя из Redis"""
async def get_balance(addr):
    #ok = await redis.set("key", "value")
    #assert ok
    #b = await redis.get(addr)
    b = 1
    print(int(b), addr)
    return int(b)

"""Асинхронная функция для загрузки информации о пользователе"""
async def send_user(addr, name, cover, desc, sign):
    print(addr, name, cover, desc, sign)
    return None

"""Асинхронная функция для загрузки транзакций"""
async def get_tx(amount, addr, msg, time, skip, limit) -> List[GraphTx]:
    if amount >= 0: amount_direction = '$gt'
    else: amount_direction = '$lt'; amount = -amount
    
    if time >= 0: time_direction = '$gt'
    else: time_direction = '$lt'; time = -amount

    q = {
        'amount': {amount_direction: amount},
        'time': {time_direction: time},
    }

    if msg != None:
        if msg == True: q['msg'] = {'$ne': 'null'}
        else: q['msg'] = 'null'

    if addr:
        q['$or'] = [{'credit': addr}, {'debit': addr}]
    
    print(q)

    return [
        GraphTx.from_pydantic(Tx(**t)) for t in await txs.find({
            '$query': q,
            '$orderby': {'_id': -1}
            })
            .skip(skip)
            .limit(limit)
            .to_list(None)
    ]

async def send_tx(tx: Tx) -> str:
    print(jsonable_encoder(tx))
    return "ok"

"""Определение класса Query для обработки GraphQL запросов"""
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
        addr: str = '',
        amount: int = 0,
        time: int = 0,
        skip: int = 0,
        limit: int = 100
    ) -> List[GraphTx]:
        return await send_tx(amount, addr, msg, time, skip, limit)
    
    @strawberry.field
    async def sendUser(
        self,
        addr: str = '',
        name: str = '',
        cover: str = '',
        desc: str = '',
        sign: str = ''
    ) -> None:
        return await send_user(addr, name, cover, desc, sign)

    @strawberry.field
    async def getBalance(
        self,
        addr: str = ''
    ) -> float:
        return await get_balance(addr)

"""Создание объекта схемы GraphQL"""
schema = strawberry.Schema(query=Query)

"""инициализация сервера GraphQL"""
graphql_app = GraphQL(schema)#graphiql=False

"""Создание объекта (веб-приложения) FastAPI"""
app = FastAPI()

"""Добавление CORS Middleware для обработки CORS-запросов"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Функция, вызываемая при запуске приложения 
для инициализации соединения с RabbitMQ и Redis"""
@app.on_event("startup")
async def startup() -> None:
    global mq
    connection = await connect_robust("amqp://guest:guest@localhost/")
    mq = await connection.channel()
    queue = await mq.declare_queue("tx", durable=True)
    global redis
    redis = await aioredis.from_url("redis://localhost",  db=0)

"""Регистрация GraphQL-маршрутов в FastAPI 
для обработки HTTP и WebSocket запросов к GraphQL API"""
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
