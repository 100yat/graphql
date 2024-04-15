from src.user.userModel import GraphUser


class UserController:
    def __init__(self):
        self.Users = {
            1: GraphUser(
                addr="123",
                name="sergeyi",
                cover="coverSergeyi",
                desc="descSergeyi",
                sign="signSergeyi",
            ),
            2: GraphUser(
                addr="456", name="Vova", cover="coverVova", desc="descVova", sign="signVova"
            ),
        }

    def get_all_user_contacts(self, user_id):
        return self.Users[1]

    def get_all_user(self):
        return list(self.Users.values())

    def get_user(self):
        return self.Users[2]

    def send_user(self, addr, name, cover, desc, sign) -> bool:
        #TODO Здесь нужно использовать GraphUser который использует @strawberry.mutations
        print(addr, name, cover, desc, sign)
        return True