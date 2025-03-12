import time
import requests

from backend.wallet.wallet import Wallet

BASE_URL ='http://127.0.0.1:5000'

def get_blockchain():
    return requests.get(f'{BASE_URL}/chain').json()


def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/mine/block').json()

def post_wallet_transact(reciver, amount):
    return requests.post(f'{BASE_URL}/wallet/send',json=
                         {'reciver':reciver, 'amount': amount}).json()
def post_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()

start_blockchian = get_blockchain()
print(start_blockchian)
reciver = Wallet().address

post_wallet_transact1 = post_wallet_transact(reciver, 1000)
print(f'\n post_wallet_transact1: {post_wallet_transact1}')

time.sleep(3)
post_wallet_transact2 = post_wallet_transact(reciver, 694)
print(f'\n post_wallet_transact2: {post_wallet_transact2}')

time.sleep(1)
mine = get_blockchain_mine()

print(f'\n mine: {mine}')

wall_info = post_wallet_info()
print(f'\n wall_info: {wall_info}')

