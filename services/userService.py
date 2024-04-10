import src.models
from src.graphqlModels import GraphUser

class UserService:
    def __init__(self):
        Users = {
            1: src.models.User(
                addr="123",
                name="sergeyi",
                cover="coverSergeyi",
                desc="descSergeyi",
                sign="signSergeyi",
            ),
            2: src.models.User(
                addr="456", name="Vova", cover="coverVova", desc="descVova", sign="signVova"
            ),
        }

    def get_all_user_contacts(self, user_id):
        return GraphUser(
            addr="123",
            name="sergeyi",
            cover="coverSergeyi",
            desc="descSergeyi",
            sign="signSergeyi",
        )

    def get_all_user(self):
        return [
            GraphUser(
                addr="123",
                name="sergeyi",
                cover="coverSergeyi",
                desc="descSergeyi",
                sign="signSergeyi",
            )
        ]

    def get_user(self):
        return GraphUser(
            addr="123",
            name="sergeyi",
            cover="coverSergeyi",
            desc="descSergeyi",
            sign="signSergeyi",
        )

    def send_user(self, addr, name, cover, desc, sign):
        print(addr, name, cover, desc, sign)
        return None