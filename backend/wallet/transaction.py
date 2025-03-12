import time 
import uuid

from backend.wallet.wallet import Wallet
from backend.config import MINE_REWARD, MINE_REWARD_INPUT
class Transaction:
    """
    Documents an exchange between a sender and reciver 
    """

    def __init__(self,sender_wallet=None,reciver=None,
                 amount=None, id=None,output=None, input=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.output = output or self.create_output(sender_wallet, reciver, amount)
        self.input = input or self.create_input(sender_wallet, self.output)
        
    def create_output(self, sender_wallet, reciver, amount):
        """
        Structure the transaction data 
        """
        if amount > sender_wallet.balance:
            raise Exception('Balance can not be negative')
        
        output = {}
        output[reciver] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount
        
        return output
        
    def create_input(self,sender_wallet, output):
        """
        Structurs the input data for the transaction
        Sign the transation and include the senders public key and address
        """
        return {
            'time': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output),
        }
    
    def update(self, sender_wallet, reciver, amount):
        """
        Updates the transaction data  with a new or existing recipient.
        """
        if amount > self.output[sender_wallet.address]:
            raise Exception('Amout exceeded balance')
        
        if reciver in self.output:
            self.output[reciver] = self.output[reciver] + amount
        else:
            self.output[reciver] = amount
        
        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount        
        self.input = self.create_input(sender_wallet, self.output)
    
    def serializer(self):
        """
        serliaze transactions obj into json format
        """
        return self.__dict__
    
    @staticmethod
    def deserializer(json_format__transaction):
        """
        Deserialize the transaction data from a json format
        """
        return Transaction(**json_format__transaction)
    
    @staticmethod   
    def is_valid_transaction(transaction):
        """
        Validate a transaction
        Raise an exception for invalid transations 
        """
        if transaction.input == MINE_REWARD_INPUT:
            if list(transaction.output.values()) != [MINE_REWARD]:
                raise Exception('Invalid mining Reward')
            return
        
        total_output = sum(transaction.output.values())
        if transaction.input['amount'] != total_output:
            raise Exception('Invalid transaction values')
        
        if not Wallet.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']):
            raise Exception('Invalid signature')
            
    @staticmethod
    def mining_reward_transaction(miner_wallet):
        """
        Gemerate a mining reward for awarding the miner of the transaction
        """
        output = {}
        output[miner_wallet.address] = MINE_REWARD
        return Transaction(input=MINE_REWARD_INPUT, output=output)
    
        
    
def main():
    wallet = Wallet()
    transaction = Transaction(wallet, 'reciver', 100)
    
    print(f'{transaction.__dict__}')
    transaction.serializer()
    
    
if __name__ == '__main__':
    main()