"""A script to test block speed"""
import time
from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS
blockchain = Blockchain()

times = []

for i in range(1000):
    star_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - star_time) / SECONDS
    times.append(time_to_mine)

    avareg_time = sum(times) / len(times)

    print(f'New Block difficultly: {blockchain.chain[-1].difficulty}')
    print(f'Time per each mined block: {time_to_mine}s')
    print(f'Average time to mine blocks: {avareg_time}s\n')
