import pytest

from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.config import MINE_REWARD_INPUT, MINE_REWARD 


def test_transaction():
    sender = Wallet()
    reciver = 'reciver'
    amount = 50
    transaction = Transaction(sender,reciver,amount)
    
    assert 'time' in transaction.input
    assert transaction.input['amount'] == sender.balance
    assert transaction.input['address'] == sender.address
    assert transaction.input['public_key'] ==sender.public_key

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )
    
    
def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Balance can not be negative'):
        Transaction(Wallet(), 'zee', 15000)
        
def test_transaction_update_exceeded_balance():
    sender = Wallet()
    transaction = Transaction(sender, 'man', 500)
    
    with pytest.raises(Exception, match='Amout exceeded balance'):
        transaction.update(sender, 'zee',15000)
        
def test_transaction_updated_balance():
    sender = Wallet()
    reciver1 = 'cheata'
    amount1 = 3000
    transaction = Transaction(sender, reciver1, amount1)
    
    reciver2 = 'obj'
    amount2 = 5000
    transaction.update(sender, reciver2, amount2)
    
    assert transaction.output[reciver2] == amount2
    assert transaction.output[sender.address] == \
        sender.balance - amount1 - amount2
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )
    
    send_to_reciver1 = 1500
    transaction.update(sender, reciver1, send_to_reciver1)
    
    assert transaction.output[reciver1] == amount1 + send_to_reciver1
    assert transaction.output[sender.address] == \
        sender.balance - amount1 - amount2 - send_to_reciver1 
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )
    
def test_vaild_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'reciver', 500))
    
def test_vaild_transaction_with_invalid_outputs():
    
    sender = Wallet()
    transaction = Transaction(sender, 'man', 500)
    transaction.output[sender.address] = 10001
    with pytest.raises(Exception, match='Invalid transaction values'):
        Transaction.is_valid_transaction(transaction)
        

def test_vaild_transaction_with_invalid_signature():
    
    transaction = Transaction(Wallet(), 'msa', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match='Invalid signature'):
        Transaction.is_valid_transaction(transaction)
    
    
def test_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transaction.mining_reward_transaction(miner_wallet)
    assert transaction.input == MINE_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINE_REWARD


def test_valid_reward_transaction():
    reward_transaction = Transaction.mining_reward_transaction(Wallet())
    Transaction.is_valid_transaction(reward_transaction)


def test_is_valid_reward_transaction_extra_miner():
    reward_transaction = Transaction.mining_reward_transaction(Wallet())
    reward_transaction.output['extra'] = 60


    with pytest.raises(Exception, match='Invalid mining Reward'):
        Transaction.is_valid_transaction(reward_transaction)


def test_valid_reward_transaction_invalid_reward():
    miner = Wallet()
    reward_transaction = Transaction.mining_reward_transaction(miner)
    reward_transaction.output[miner.address] = 2500

    with pytest.raises(Exception, match='Invalid mining Reward'):
        Transaction.is_valid_transaction(reward_transaction)
