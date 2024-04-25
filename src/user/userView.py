from pprint import pprint

import strawberry
from src.user.userController import UserController
from src.user.userModel import GraphUser


@strawberry.type
class UserQuery:
    @strawberry.field
    async def sendUser(
        self,
        addr: str = "",
        name: str = "",
        cover: str = "",
        desc: str = "",
        sign: str = "",
    ) -> GraphUser:
        return await UserController().send_user(addr, name, cover, desc, sign)

    @strawberry.field
    async def getUser(self, Id: str) -> GraphUser:
        return await UserController().get_user(str(Id))

    @strawberry.field
    async def allUser(self) -> list[GraphUser]:
        users_res = await UserController().get_all_user()
        return users_res

    @strawberry.field()
    def get_all_user_contacts(self, user_id: str) -> GraphUser:
        return UserController().get_all_user_contacts(user_id)
