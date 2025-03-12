import time
from backend.utils.hasher import hasher
from backend.config import MINE_RATE
from backend.utils.hex_to_bin import hex_to_bin


GENNSIS_DATA = {'time_stamp':1, 'hashed':'gennsis_hash',
                'last_hash':'gennsis_last_hash', 'data':[], 
                'difficulty': 3, 'nonce': 'gennsis_nonce'}

class Block:
    """Stores a transaction in a block"""

    def __init__(self,data, hashed, last_hash, time_stamp, difficulty, nonce):
        self.data = data
        self.time_stamp = time_stamp
        self.hashed = hashed
        self.last_hash = last_hash
        self.difficulty = difficulty
        self.nonce = nonce

    def __str__(self):
        return self.data

    def __eq__(self, value):
        return self.__dict__ == value.__dict__
    
    def serializer(self):
        """Serializers the block for json usage"""
        return self.__dict__
    
    def __repr__(self):
        return(
            "Block ("
                f"Data: {self.data}, "
                f"Last Hashed: {self.last_hash} "
                f"Hash: {self.hashed}, "
                f"Time: {self.time_stamp}, "
                f"difficulty: {self.difficulty}, "
                f"Nonce: {self.nonce}, "
            ")"
        )
    @staticmethod
    def mine_block(last_block, data):
        """
        given an in put of the last mined block,
        mines a new block until the proof of work requirments are met.
       """
        timer = time.time_ns()
        last_hash = last_block.hashed
        difficulty = Block.difficulty_ctlr(last_block, timer)
        nonce = 0
        hashed = hasher(timer, last_hash, data, difficulty, nonce)


        while hex_to_bin(hashed)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timer = time.time_ns()
            hashed = hasher(timer, last_hash, data, difficulty, nonce)
        
        return Block(data=data, hashed=hashed, last_hash=last_hash, time_stamp=timer, difficulty=difficulty, nonce=nonce)
    

    @staticmethod
    def gennsis():
        """Generates the first block"""
        return Block(**GENNSIS_DATA)
    
    @staticmethod
    def from_json(block):
        """Deserializes a blocks json representation back into a block instance"""
        return Block(**block)

    @staticmethod
    def difficulty_ctlr(last_block, new_timer):
        """
        adjust mining difficulty on based on the MINE_RATE and adjusts the up or down 
        """
        if (new_timer - last_block.time_stamp) < MINE_RATE:
            return  last_block.difficulty + 1
        if (last_block.difficulty) > 0:
            return last_block.difficulty - 1
        return 1
    
    @staticmethod
    def is_vaild_block(last_block, block):
        """Validate Block with in the following rules:
            - The block must have the proper last_hash reference
            - The Block must meet the proof of work requirment
            - The difficulty must only incremnet by 1
            - The Block hash must be a valid combo field of the Block
        """
       

        if block.last_hash != last_block.hashed:
            raise Exception('The block must have the proper hash references to the pre hash')

        if hex_to_bin(block.hashed)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The block must meet the proof of work requirment')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception("The difficulty must only incremnet by 1")
        
        
        reconstructed_hash = hasher(
            block.data,
            block.last_hash,
            block.time_stamp,
            block.nonce,
            block.difficulty,)
            
        if block.hashed != reconstructed_hash:
            raise Exception ('The block must meet the proof of work requirment')
            # raise Exception("The block hash must be a valid")



def main():
    """Testing: Runs Main File Only"""
    gennie = Block.gennsis()
    bad = Block.mine_block(gennie,'bad')
#check to see that the last hash has changed
    # bad.last_hash = 'bad-bad'

# test to check if difficulty changed
    # jumped = 10
    # bad.difficulty = jumped
    # bad.hashed = f'{"0"* jumped}' 

# checks for corrupted hash
    bad.hashed = "0000000000000000achx" 

# check to see if the hash hash changed
    # bad.hashed = '420'
    # print(bad.last_hash)


    # print(bad.last_hash)

    try:
        Block.is_vaild_block(gennie,bad)
    except Exception as e:
        print(f'Validation Error: {e}')
if __name__ == '__main__':
    main()