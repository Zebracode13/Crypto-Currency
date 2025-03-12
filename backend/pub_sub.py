
import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

pn_config = PNConfiguration()

pn_config.subscribe_key ='sub-c-309c3f7f-343d-43af-abad-8521d645e9ce'
pn_config.publish_key = 'pub-c-df36fb95-9463-47cd-836f-62168a859fd0'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK':'BLOCK',
    'TRANSACTION': 'TRANSACTION',
}

class Listener(SubscribeCallback):

    def __init__(self,blockchain,transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        
    def message(self, pubnub, json_message):
        print(f'\n-- channel: {json_message.channel} | {json_message.message}')
        
        if json_message.channel == CHANNELS['BLOCK']:
            block = Block.from_json(json_message.message)
            potent_chain = self.blockchain.chain[:] 
            potent_chain.append(block)
            try:
                self.blockchain.replace_chain(potent_chain)
                self.transaction_pool.clear_blockchain_transaction(self.blockchain)
                print(f"\n -- Chian replaced")              
            except Exception as e:
                print(f"\n -- Did not replace chain {e}")      
        elif json_message.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.deserializer(json_message.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n ---The new transaction has been set in the transaction store')
            
                        
class PubSub():
    """
    Handles the the publisher/subscriber layer of the application
    Provides Commuincation between the nides f the blockchain network
    """
    def __init__(self,blockchain,transaction_pool):
        self.pubnub = PubNub(pn_config)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute() 
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self,channel,message):
        """
        Plublis the message objext to the channel
        """
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()
        
    def broadcast_block(self,block):
        """
        Bradcats the block as a json
        """
        self.publish(CHANNELS['BLOCK'],block.serializer())
        
        
    def broadcast_transaction_pool(self,transaction):
        """
        Bradcats the block as a json
        """
        self.publish(CHANNELS['TRANSACTION'],transaction.serializer())



def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'],{'foo': 'poo'} )

if __name__ == '__main__':
    main()
