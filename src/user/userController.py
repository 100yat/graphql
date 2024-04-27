from pprint import pprint

from src.user.userModel import GraphUser, User
import main
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorChangeStream
from typing import Any
from bson import ObjectId


class UserController:
    def __init__(self):
        self.users: AsyncIOMotorCollection = main.users
        # self.Users = {
        #     1: GraphUser(
        #         addr="123",
        #         name="sergeyi",
        #         cover="coverSergeyi",
        #         desc="descSergeyi",
        #         sign="signSergeyi",
        #     ),
        #     2: GraphUser(
        #         addr="456",
        #         name="Vova",
        #         cover="coverVova",
        #         desc="descVova",
        #         sign="signVova",
        #     ),
        # }

    async def get_all_user_contacts(self, user_id):
        self.users.findOne()
        return self.users.find()

    async def get_all_user(self):
        users_result = self.users.find()
        tt = await users_result.to_list(length=100)
        print("values == ", tt[0].values())
        print("items == ", tt[0].items())
        print("get == ", tt[0].get("Addr"))
        print("keys == ", tt[0].keys())
        result = []
        for t in tt:
            if (
                "addr" in t.keys()
                and "name" in t.keys()
                and "cover" in t.keys()
                and "desc" in t.keys()
                and "sign" in t.keys()
            ):
                result.append(
                    GraphUser(
                        addr=t.get("addr"),
                        name=t.get("name"),
                        cover=t.get("cover"),
                        desc=t.get("desc"),
                        sign=t.get("sign"),
                    )
                )
        return result

    async def get_user(self, Id: str):
        cursor = await self.users.find_one({"_id": ObjectId(Id)})
        user = User(**cursor)
        user.Id = cursor.get("_id")
        return user

    async def get_user_ws(self, Id: str):
        #TODO Возможно сделать пул со сравнением какую коллекцию отслеживать
        async with self.users.watch() as stream:
            stream: AsyncIOMotorChangeStream
            # while stream.next():
            #     pprint(stream)
            async for change in stream:
                print("change")
                pprint(change)
                _id_user_event = ObjectId(change["documentKey"]["_id"])
                updateFields = change["updateDescription"]["updatedFields"]
                print(f"Id {Id}")
                print(f"_id_user_event {_id_user_event}")
                print(f"updateFields.keys() {list(updateFields.keys())}")
                print(f"\"balance\" in updateFields.keys() {'balance' in list(updateFields.keys())}")
                if Id == str(_id_user_event) and "balance" in list(updateFields.keys()):
                    cursor = await self.users.find_one({"_id": _id_user_event})
                    user = User(**cursor)
                    user.Id = cursor.get("_id")
                    print("Делаем елд")
                    yield user
        # return user

    async def send_user(self, addr, name, cover, desc, sign) -> Any:
        # TODO Здесь нужно использовать GraphUser который использует @strawberry.mutations
        print(addr)
        print(name)
        print(cover)
        print(desc)
        print(sign)
        # print(User(addr=addr, name=name, cover=cover, desc=desc, sign=sign))
        userModel = User(addr=addr, name=name, cover=cover, desc=desc, sign=sign)
        user = await self.users.insert_one(
            userModel.dict()
        )
        if user.acknowledged:
            userModel.Id = user.inserted_id
            graph_user = GraphUser(Id=user.inserted_id, addr=addr, name=name, cover=cover, desc=desc, sign=sign)
            return graph_user
        return "error"
