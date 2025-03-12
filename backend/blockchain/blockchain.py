from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import MINE_REWARD_INPUT
from backend.wallet.wallet import Wallet
class Blockchain:
    """A Block chain stores blocks in a list"""
    def __init__(self):
        self.chain = [Block.gennsis()]
        self.block_count = len(self.chain)

    def __repr__(self):
        return f"Blockchain: {self.chain}"
    
    def __str__(self):
        return str(self.chain)

    def add_block(self, data):
        """Given input of data and last block adds to the end of the block chain list"""
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def replace_chain(self, chain):
        """
        Replace the level chian with the incoming if the following applies:
            - The incoming chain is longer that the local one.
            - The incoming chain is formatted proprly
        """

        if len(self.chain) >= len(chain):
            raise Exception("The chain must be longer than local chain")
        
        try:
            Blockchain.validate_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace, the format is not correct: {e}')
        self.chain = chain

    def serializer(self):
        """Serializers the data for json usage"""
        # serial = []
        return list(map(lambda block:block.serializer(), self.chain))
        # for block in self.chain:
        #     serial.append(block.serializer())
        # return serial
    def deserializer(json_chain):
        """
        Deseraizes a list of serialized blxks int a Blockchain instances
        The reslut will contain a chain list of Blocks instances 
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda json_block: Block.from_json(json_block), json_chain))
        return blockchain
    @staticmethod
    def validate_chain(chain):
        """Validates incoming chain
            - The block must start with gennsis
            - Blocks must be formated correctly
        """
        if chain[0] != Block.gennsis():
            raise Exception ("The gennsis block must be the valid")
        for i in range(1, len(chain)):
            Block.is_vaild_block(chain[i-1], chain[i])
            
        Blockchain.is_valid_trasaction_chain(chain)
        
    @staticmethod
    def is_valid_trasaction_chain(chain):
        """
        Will enforce the rules a chain coposed of blocks of transaction
            - Each transaction must only appear once in the chain
            - There can only be one mining rewad per block.
            - Each transation must be valid
        """
        transaction_id = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            
            for transaction_json in block.data:
                
                current_transaction = Transaction.deserializer(transaction_json)
                
                            
                if current_transaction.id in transaction_id:
                    raise Exception(f"Not unique trasnsation id {current_transaction.id}")
                
                transaction_id.add(current_transaction.id)
                       
                if current_transaction.input == MINE_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(f"Mining reward already exists {block.hashed}")
    
                    has_mining_reward = True
                else:
                    historical_blockchain = Blockchain()
                    historical_blockchain.chain = chain[0:i]
                    historical_balance = Wallet.calculate_balance(
                        current_transaction.input['address'],
                        historical_blockchain
                    )
                
                    if historical_balance != current_transaction.input['amount']:
                        raise Exception(f"Transaction has an invalid input amount {current_transaction.id}")
                    
                Transaction.is_valid_transaction(current_transaction)
                
                
        
        
            
def main():
    "Main file runner method"
    bc = Blockchain()
    bc.add_block('100',)
    bc.add_block('5')
    print(bc.chain)
    print(bc.validate_chain(bc.chain))
if __name__ == '__main__':
    main()
