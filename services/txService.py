from src.models import Tx
from src.graphqlModels import GraphTx
from typing import List
from fastapi.encoders import jsonable_encoder


class TxService:
    def __init__(self, txs):
        self.txs = txs

    def get_all_TX(self):
        """

        :return:
        """
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
            amount_direction = '$gt'
        else:
            amount_direction = '$lt'; amount = -amount

        if time >= 0:
            time_direction = '$gt'
        else:
            time_direction = '$lt'; time = -amount

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

    def send_tx(self, tx: Tx):
        print(jsonable_encoder(tx))
        return "ok"

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