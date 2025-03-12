import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENNSIS_DATA
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

@pytest.fixture
def create_blocks_in_blockchain():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), 'reciver', i).serializer()])
    return blockchain

def test_blockchain_instance(create_blocks_in_blockchain):
    """Test the create of the chain"""
    assert create_blocks_in_blockchain.chain[0].hashed == GENNSIS_DATA['hashed']

def test_add_block(create_blocks_in_blockchain):
    """tests to see if a new block was mined and added to the chain"""
    data = 'test-data'
    create_blocks_in_blockchain.add_block(data)
    new_data =  create_blocks_in_blockchain.chain[-1].data
    assert new_data == data 

def test_chain_validation(create_blocks_in_blockchain):
    """Test the valdation of the chain"""
    Blockchain.validate_chain(create_blocks_in_blockchain.chain)

def test_chain_bad_validation(create_blocks_in_blockchain):
    """Test the valdation of the chain"""
    create_blocks_in_blockchain.chain[0].hash = 'corrupted'
    with pytest.raises(Exception, match="The gennsis block must be the valid"):
        Blockchain.validate_chain(create_blocks_in_blockchain.chain)
    
def test_replace_chain(create_blocks_in_blockchain):
    blockchain = Blockchain()
    blockchain.replace_chain(create_blocks_in_blockchain.chain)

    assert blockchain.chain == create_blocks_in_blockchain.chain


def test_replace_chain_not_longer(create_blocks_in_blockchain):
    blockchain = Blockchain()

    with pytest.raises(Exception, match="The chain must be longer than local chain"):
        create_blocks_in_blockchain.replace_chain(blockchain.chain)


def test_replace_chain_invalid_chain(create_blocks_in_blockchain):
    blockchain = Blockchain()
    create_blocks_in_blockchain.chain[1].hashed = 'corrupted'

    with pytest.raises(Exception, match='o'):
        blockchain.replace_chain(create_blocks_in_blockchain.chain)

def test_valid_transaction_chain(create_blocks_in_blockchain):
    Blockchain.is_valid_trasaction_chain(create_blocks_in_blockchain.chain)


def test_is_valid_trasaction_chain_dublicate(create_blocks_in_blockchain):
    transaction = Transaction(Wallet(), 'reciver', 200).serializer()
    create_blocks_in_blockchain.add_block([transaction, transaction])
    
    with pytest.raises(Exception, match='Not unique trasnsation id'):
        Blockchain.is_valid_trasaction_chain(create_blocks_in_blockchain.chain)

def test_is_valid_trasnaction_chain_mutiple_rewards(create_blocks_in_blockchain):
    reward_1 = Transaction.mining_reward_transaction(Wallet()).serializer()
    reward_2 = Transaction.mining_reward_transaction(Wallet()).serializer()
    create_blocks_in_blockchain.add_block([reward_1, reward_2])
    
    with pytest.raises(Exception, match='Mining reward already exists'):
        Blockchain.is_valid_trasaction_chain(create_blocks_in_blockchain.chain)
    
def test_is_valid_transaction_bad_chain(create_blocks_in_blockchain):
    bad_transaction = Transaction(Wallet(), 'reciver', 1)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    create_blocks_in_blockchain.add_block([bad_transaction.serializer()])
    
    with pytest.raises(Exception):
        Blockchain.is_valid_trasaction_chain(create_blocks_in_blockchain.chain)
    
def test_is_valid_transaction_chain_bad_balance_report(create_blocks_in_blockchain):
    wal = Wallet()
    bad_transaction = Transaction(wal, 'reciver', 1)
    bad_transaction.output[wal.address] = 9000
    bad_transaction.input['amount'] = 9001
    bad_transaction.input['signature'] = wal.sign(bad_transaction.output)
    
    create_blocks_in_blockchain.add_block([bad_transaction.serializer()])

    with pytest.raises(Exception, match='Transaction has an invalid input amount'):
        Blockchain.is_valid_trasaction_chain(create_blocks_in_blockchain.chain)






