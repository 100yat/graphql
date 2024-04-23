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
