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
    ) -> bool:
        return UserController().send_user(addr, name, cover, desc, sign)

    @strawberry.field
    def getUser(self, _id: int) -> GraphUser:
        return UserController().get_user()

    @strawberry.field
    def get_all_user(self) -> list[GraphUser]:
        return UserController().get_all_user()

    @strawberry.field()
    def get_all_user_contacts(self, user_id: int) -> GraphUser:
        return UserController().get_all_user_contacts(user_id)

