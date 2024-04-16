import time
import random
import uuid
import base58
import hashlib
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from src.models import Ask, Vote
from pymongo import MongoClient

cli = MongoClient('localhost', 27017)

db = cli.yat
txs = db.tx
asks = db.asks
votes = db.votes

def tob2b(transaction):
    """хеширование данных алгоритмом BLAKE2b и кодирование в формат Base58
    t - транзакция?"""
    hash = hashlib.blake2b()
    hash.update(transaction)
    return base58.b58encode(hash.digest())

"""реализовать получение / генерацию secret_key и public_key"""
secret_key = 'DQsYfHpJ9WAGai9JJ1eDntkx4CpeCAbhPi2MrPDiwYs5'
secret_key_bytes = base58.b58decode(secret_key.encode())
public_key = 'B3qUs7s5C5G4n7V5x2XE4JMWzPMvVXWRzkxfp76zgs6t'

amount = 1000000000000
unique_id = str(uuid.uuid4())
message = public_key + str(amount) + str(unique_id)
signing_key = SigningKey(secret_key_bytes)
encoded_message = bytes(message.encode("utf-8"))
signed_ask = base58.b58encode(signing_key.sign(encoded_message))
hash_ask = tob2b(signed_ask)

new_ask = Ask(address = public_key,
    amount = amount,
    unique_id = unique_id,
    title = '',
    cover = '',
    desc = '',
    sign = signed_ask,
    prev_hash = '',
    hash = hash_ask,
    time = int(round(time.time() * 1000)))

added_ask = asks.insert_one(dict(new_ask))
if added_ask.inserted_id:
    print(added_ask.inserted_id)

unique_vote_id = str(uuid.uuid4())
like = True
message = public_key + str(hash_ask) + str(like) + str(unique_id)
encoded_message = bytes(message.encode("utf-8"))
signed_vote = base58.b58encode(signing_key.sign(encoded_message))
hash_vote = tob2b(signed_vote)

new_vote = Vote(address = public_key,
    id = hash_ask,
    like = like,
    unique_id = unique_id,
    sign = signed_vote,
    prev_hash = '',
    hash = hash_vote,
    time = int(round(time.time() * 1000)))

added_vote = votes.insert_one(dict(new_vote))
if added_vote.inserted_id:
    print(added_vote.inserted_id)    

print(new_ask)
print(new_vote)
