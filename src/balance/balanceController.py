from src.balance.balanceModel import Balance, GraphBalance
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List
from src.user.userModel import User
from src.transaction.transactionModel import Tx, GraphTx
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
import math
from pymongo import MongoClient
import logging

"""
class BalanceController:
    def __init__(self):
        pass

    def get_balance(self, addr):
        # ok = await redis.set("key", "value")
        # assert ok
        # b = await redis.get(addr)
        b = 1
        print(int(b), addr)
        return int(b)

import redis
from src.models import Ask, Vote, Tx, User
redis = redis.Redis(host='localhost', port=6379, db=0)
"""

logfmt = '%(levelname)s | %(message)s'
logging.basicConfig(level=logging.DEBUG, format=logfmt)
logging.basicConfig(level=logging.INFO, format=logfmt) #handlers=loghdlrs
logging.basicConfig(level=logging.WARNING, format=logfmt)
logging.basicConfig(level=logging.ERROR, format=logfmt)
logging.getLogger().setLevel(logging.INFO)

cli = MongoClient('localhost', 27017)
db = cli.yat
db_tx = db.tx
db_users = db.users


class BalanceController:
    def __init__(self, db: AsyncIOMotorCollection):
        self.txs: AsyncIOMotorCollection = db.tx
        self.users: AsyncIOMotorCollection = db.users

    async def get_all_Balances(self) -> List[GraphBalance]:
        all_balances = []
        balances_q = self.txs.find()
        async for balance in balances_q:
            all_balances.append(GraphBalance(**balance, id=balance['_id']))
        return all_balances
    

    async def get_balance(self, addr) -> GraphBalance:
        # user_id = await self.users.find_one({"addr": addr})
        amount = 0
        cursor_user_credit = await self.txs.find_one({"credit": addr})
        cursor_user_debit = await self.txs.find_one({"debit": addr})
        user_credit_amount = int(sum(**cursor_user_credit.get("amount")))
        user_debit_amount = int(sum(**cursor_user_debit.get("amount")))
        amount = user_debit_amount - user_credit_amount
        q = {"amount": {amount}}
        return GraphBalance(amount)


    async def get_balance_by_user(self, user_id: ObjectId) -> GraphBalance:
        balance_q = await self.users.find_one({'_id': ObjectId(user_id)})
        if balance_q:
            return GraphBalance(**balance_q, id=balance_q['_id'])
        return GraphBalance()



"""
tx = db_tx.find({})
users = db_users.find({})

balances = {}
netto = {}

def emission() -> int:
    return int(sum(balances.values()) or 1)

def addr_balance(addr: str) -> int:
    return int(balances.get(addr) or 1)

def addr_current_balance(addr: str):
    asks_current = addr_asks(addr)
    print(asks_current)
    b = 1
    for ask in asks_current:
        b += ask_balance(ask)
    return b + int(netto.get(addr) or 0)

def calc_balances():
    for _ in range(5):
        for u in users:
            u = User(**u)
            print(u)
            b = addr_current_balance(u.addr)
            balances.update({u.addr: b})

def calc_tx():
    for t in tx:
        t = Tx(**t)
        c = netto.get(t.credit)
        d = netto.get(t.debit)
        netto.update({t.credit: int(c or 0) - t.amount})
        netto.update({t.debit: int(d or 0) + t.amount})

for i in range(5):
    calc_balances()
    print(f'{i} Balances: {balances}')

for b in balances:
    redis.set(b, balances[b])

def addr_asks(addr: str) -> List:
    a = []
    asks = db_asks.find({})
    for ask in asks:
        ask = Ask(**ask)
        if ask.addr == addr:
            a.append(ask.hash)
    return a

def addr_karma(addr: str) -> int:
    return addr_balance(addr) / emission()

def ask_votes(id: str) -> List:
    v = []
    votes = db_votes.find({})
    for vote in votes:
        vote = Vote(**vote)
        if vote.id == id:
            v.append(vote.addr)
    return v

def ask_balance(id: str) -> int:
    balance = 0
    ask = db_asks.find_one({"hash": id})
    ask = Ask(**ask)
    for vote in ask_votes(id):
        k = addr_karma(vote)
        balance += ask.amount * k
    return math.floor(balance)
"""

