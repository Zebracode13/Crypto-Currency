from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.config import STARTING_BALANCE


def test_wallet_verfied():
    """
    Tests the signature was validated: 
    """
    data = {'test': 'data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    
    assert Wallet.verify(wallet.public_key, data, signature)


def test_wallet_verfied_invalid():
    """
    Tests the signature was validated: 
    """
    data = {'test': 'data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    
    assert Wallet.verify(Wallet().public_key, data, signature) == False


def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()
    assert Wallet.calculate_balance(wallet, blockchain) == STARTING_BALANCE

    amount = 2500
    transaction = Transaction(wallet, 'zee', amount)

    blockchain.add_block([transaction.serializer()])
    assert Wallet.calculate_balance(wallet, blockchain) == STARTING_BALANCE

    recived_1 = 200
    recived_1 = 1500

    recived_1_trans = Transaction(Wallet(), wallet.address, recived_1)
    recived_2_trans = Transaction(Wallet(), wallet.address, recived_1)

    blockchain.add_block([recived_1_trans.serializer(), 
                          recived_2_trans.serializer()])
    assert Wallet.calculate_balance(wallet.address, blockchain)
    