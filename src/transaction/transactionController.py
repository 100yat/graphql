from pprint import pprint

from src.transaction.transactionModel import Tx, GraphTx
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List
from src.user.userModel import User
from src.transaction.transactionModel import Tx, GraphTx
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


class TransactionController:
    def __init__(self, db: AsyncIOMotorCollection):
        self.txs: AsyncIOMotorCollection = db.tx
        self.users: AsyncIOMotorCollection = db.users

"""
    def get_all_TX(self):
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
"""
    async def get_all_TX(self) -> List[GraphTx]:
        all_TX = []
        txs_q = self.txs.find()
        async for t in txs_q:
            all_TX.append(GraphTx(**t, id=t['_id']))
        return all_TX


    def get_tx(self, amount, addr, msg, time, skip, limit) -> List[GraphTx]:
        if amount >= 0:
            amount_direction = "$gt"
        else:
            amount_direction = "$lt"
            amount = -amount

        if time >= 0:
            time_direction = "$gt"
        else:
            time_direction = "$lt"
            time = -amount

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
            for t in self.txs.find({"$query": q, "$orderby": {"_id": -1}})
            .skip(skip)
            .limit(limit)
            .to_list(None)
        ]

    async def send_tx(self, tx: Tx):
        tx_write = await self.txs.insert_one(tx.dict())

        cursor_from_user = await self.users.find_one({"_id": ObjectId(tx.fromUserId)})
        cursor_to_user = await self.users.find_one({"_id": ObjectId(tx.toUserId)})
        pprint(cursor_from_user)
        if not cursor_from_user:
            return "not found from User"
        if not cursor_to_user:
            return "not found to User"
        from_user = User(**cursor_from_user)
        from_user.Id = str(cursor_from_user.get("_id"))
        to_user = User(**cursor_to_user)
        to_user.Id = str(cursor_to_user.get("_id"))

        if tx_write.acknowledged:
            from_user.balance -= tx.amount
            to_user.balance += tx.amount
            cursor_from_user_update = await self.users.update_one({"_id": ObjectId(from_user.Id)},
                                                                  {"$set": {"balance": from_user.balance}})
            cursor_to_user_update = await self.users.update_one({"_id": ObjectId(to_user.Id)},
                                                                  {"$set": {"balance": to_user.balance}})
            print(from_user.Id)
            print(tx.amount)
            print(from_user.balance)
            print("cursor_from_user_update ", cursor_from_user_update.modified_count)
            print("cursor_to_user_update ", cursor_to_user_update.modified_count)
            tx_id = tx_write.inserted_id
            graph_tx = GraphTx(**tx.dict())
            return graph_tx
        return "error"
"""
    def get_TX_by_user(self, user_id):
        return GraphTx(
            credit="123",
            debit="321",
            amount=123.456,
            time=1234567890,
            hash="123qwe",
            msg="message qwe123",
            sign="sign что бы это не значило",
        )
"""
    async def get_TX_by_user(self, user_id: ObjectId) -> GraphTx:
        t_q = await self.txs.find_one({'_id': ObjectId(user_id)})
        if t_q:
            return GraphTx(**t_q, id=t_q['_id'])

"""
    def get_TX_by_id(self):
        return GraphTx(
            credit="123",
            debit="321",
            amount=123.456,
            time=1234567890,
            hash="123qwe",
            msg="message qwe123",
            sign="sign что бы это не значило",
        )
"""
    async def get_TX_by_id(self, _id: ObjectId) -> GraphTx:
        t_q = await self.txs.find_one({'_id': ObjectId(tx_id)})
        if t_q:
            return GraphTx(**t_q, id=t_q['_id'])
