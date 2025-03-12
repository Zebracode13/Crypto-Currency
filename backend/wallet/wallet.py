import uuid
import json 


from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature,decode_dss_signature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from backend.config import STARTING_BALANCE

class Wallet:
    """
    An indivdual wallet for miner
    Keeps transactions of minors balance
    Allows a miner to authenticate a transaction
    
    """
    
    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.public_key_serializer()

    @property
    def balance(self): 
        return Wallet.calculate_balance(self.address, self.blockchain)
        
    def sign(self, data):
        """
        Generates a signatiere based on the data using the local private key
        """
        return decode_dss_signature(
            self.private_key.sign(
            json.dumps(data).encode('utf-8'),
            ec.ECDSA(hashes.SHA256()))
        )
        
    def public_key_serializer(self):
        """
        Serailize teh public key
        """
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode('utf-8')
    

    @staticmethod
    def verify(public_key, data, sign):
        """Verify a signature based on the orginal key and data."""
        
        deserialized_public_key =  serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        
        (r,s) = sign
        
        try:
            deserialized_public_key.verify(
                encode_dss_signature(r,s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False
        
    @staticmethod
    def calculate_balance(address, blockchain):
        """
        Recalculates balance given the address as the transaction data within a blockchaiin
        
        The balance is found by adding the output values that belong to the address since
        the most recnt transaction is by transaction address
        """           
        balance = STARTING_BALANCE
        if not blockchain:
            return balance
        
        for chain in blockchain.chain:
            for transactions in chain.data:
                if transactions['input']['address'] == address:
                    # anytime the addressc= makes a new transavtion it resets the balance
                    balance = transactions['output'][address]
                elif address in transactions['output']:
                    balance +=  transactions['output'][address]
        return balance

def main():
    "run main file"
    wallet = Wallet()
    print(f'wallet: {wallet.__dict__}')
    data = {'foo': 'poo'}
    signature = wallet.sign(data)
    
    print(f'Signature: {signature}')
    
    val = wallet.verify(wallet.public_key, data, signature)
    
    print(f'Verified: {val}')
    bad = wallet.verify(Wallet().public_key, data, signature)
    print(f'Verified: {bad}')
    
if __name__ == '__main__':
    main()
