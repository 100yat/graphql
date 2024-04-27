from pprint import pprint

from src.transaction.transactionModel import Tx, GraphTx
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List
from src.user.userModel import User
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


class TransactionController:
    def __init__(self, db: AsyncIOMotorCollection):
        self.txs: AsyncIOMotorCollection = db.tx
        self.users: AsyncIOMotorCollection = db.users

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
        cursor_credit_user = await self.users.find_one({"addr": tx.credit})
        cursor_debit_user = await self.users.find_one({"addr": tx.debit})
        pprint(cursor_credit_user)
        if not cursor_credit_user:
            return "not found from User"
        if not cursor_debit_user:
            return "not found to User"
        credit_user = User(**cursor_credit_user)
        credit_user.Id = str(cursor_credit_user.get("addr"))
        debit_user = User(**cursor_debit_user)
        debit_user.Id = str(cursor_debit_user.get("addr"))

        tx_write = await self.txs.insert_one(tx.dict())
        if tx_write.acknowledged:
            credit_user.balance -= tx.amount
            debit_user.balance += tx.amount
            cursor_credit_user_update = await self.users.update_one({"addr": credit_user.Id},
                                                                  {"$set": {"balance": credit_user.balance}})
            cursor_debit_user_update = await self.users.update_one({"addr": debit_user.Id},
                                                                  {"$set": {"balance": debit_user.balance}})
            print(credit_user.Id)
            print(tx.amount)
            print(credit_user.balance)
            print("cursor_from_user_update ", cursor_credit_user_update.modified_count)
            print("cursor_to_user_update ", cursor_debit_user_update.modified_count)
            tx_id = tx_write.inserted_id
            graph_tx = GraphTx(**tx.dict())
            graph_tx.Id = tx_id
            return graph_tx
        return "error"

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
