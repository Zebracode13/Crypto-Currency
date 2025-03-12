from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain

def test_set_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'mee', 1000)
    transaction_pool.set_transaction(transaction)
    
    assert transaction_pool.transaction_store[transaction.id] == transaction

def test_clear_transactions():
    transact_pool = TransactionPool()
    transaction1 = Transaction(Wallet(), 'bab', 1000)
    transaction2 = Transaction(Wallet(), 'mee', 2000)
    
    transact_pool.set_transaction(transaction1)
    transact_pool.set_transaction(transaction2)

    chain = Blockchain()
    chain.add_block([transaction1.serializer(), transaction2.serializer()])

    assert transaction1.id in transact_pool.transaction_store
    assert transaction2.id in transact_pool.transaction_store

    transact_pool.clear_blockchain_transaction(chain)

    assert not transaction1.id in transact_pool.transaction_store
    assert not transaction2.id in transact_pool.transaction_store

