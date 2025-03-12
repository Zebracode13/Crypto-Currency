import os
import random
import requests

from flask import Flask, jsonify,request
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction_pool import TransactionPool

from backend.pub_sub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain,transaction_pool)


@app.route('/test')
def route_test():
    
    return "Testing Block"

@app.route('/chain')
def route_blockchain_detail():
    return jsonify(blockchain.serializer()) 


@app.route('/mine/block')
def route_mine_a_block():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.mining_reward_transaction(wallet).serializer())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transaction(blockchain)
    
    return jsonify(block.serializer())
   
@app.route('/wallet/send', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)
    
    if transaction:
        transaction.update(
            wallet,
            transaction_data['reciver'],
            transaction_data['amount'])
    else:
        transaction = Transaction(
            wallet,
            transaction_data['reciver'],
            transaction_data['amount'])
 
    pubsub.broadcast_transaction_pool(transaction)
    transaction_pool.set_transaction(transaction)
    
    return jsonify(transaction.serializer())   
    
    
@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({
        'addres': wallet.address, 'balance': wallet.balance
    })


# eNVIRMENT VARIALVLE:
ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    result = requests.get(f'http://localhost:{ROOT_PORT}/chain')

    result_blockchain = Blockchain.deserializer(result.json())
    
    try:
        print('-----------------------------------------------------------------')
        print('------------ Succsessfully synchronized the local chain----------')        
        print(f'-----------------------------------------------------------------\n')
        blockchain.replace_chain(result_blockchain.chain)
        
    except Exception as e:
        print('-----------------------------------------------------------------')
        print(f'Failed to replace chain {e} ')        
        print('-----------------------------------------------------------------\n')
        
app.run(port=PORT)
