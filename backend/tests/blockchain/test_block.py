import time
import pytest
from backend.blockchain.block import Block, GENNSIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_bin import hex_to_bin

def test_mine_block():
    """Test the static method for mining a block"""

    last_block = Block.gennsis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data 
    assert block.last_hash == last_block.hashed
    assert hex_to_bin(block.hashed)[0:block.difficulty] == '0' * block.difficulty

def test_gennsis():
    """Test the creatation gennsis block"""

    gen = Block.gennsis()

    assert isinstance(gen, Block)
    for key,val in GENNSIS_DATA.items():
        assert getattr(gen, key) == val

def test_difficulty_to_easy():
    """Tests the to see diffculty on the mining was to easy"""
    last_block = Block.mine_block(Block.gennsis(), 'foo')
    new_block = Block.mine_block(last_block, 1)

    assert new_block.difficulty == last_block.difficulty + 1

def test_difficulty_to_hard():
    """Tests the to see diffculty on the mining was to easy"""
    last_block = Block.mine_block(Block.gennsis(),'foo')
    time.sleep(MINE_RATE/SECONDS)
    new_block = Block.mine_block(last_block, 1)

    assert  new_block.difficulty == last_block.difficulty - 1

def test_block_diffuclty_limit_at_1():
    """tests the diffculty is greater than 0"""
    last_block = Block(
        'test-data',
        'test_hash',
        'test_last_hash',
        time.time_ns(),
        2,
        0,
    )
    time.sleep(MINE_RATE/SECONDS)

    mined_block = Block.mine_block(last_block,'loo')
    assert mined_block.difficulty == 1

@pytest.fixture
def last_block():
    return Block.gennsis()

@pytest.fixture
def created_block(last_block):
    return Block.mine_block(last_block, 'test-data')

def test_is_valid_block(last_block, created_block):
    created_block.is_vaild_block(last_block, created_block)

def test_is_valid_block_bad_last_hash(last_block, created_block):

    created_block.last_hash = 'currupted-date'
    with pytest.raises(Exception, match='The block must have the proper hash references to the pre hash'):
        Block.is_vaild_block(last_block, created_block)

def test_is_vaild_block_bad_proof_of_work(last_block, created_block):

    created_block.hashed = 'fff'
    with pytest.raises(Exception, match='The block must meet the proof of work requirment'):
        Block.is_vaild_block(last_block, created_block)

def test_is_valid_block_diff_adjusted_to_much(last_block, created_block):

    jumped =10
    created_block.difficulty = jumped
    created_block.hashed = f'{"0"* jumped}'
    with pytest.raises(Exception, match='The difficulty must only incremnet by 1'):
        Block.is_vaild_block(last_block, created_block)

def test_is_valid_block_bad_hash(last_block, created_block):

    created_block.hashed =  '000000000000000000000000hihi'
    with pytest.raises(Exception, match='h'):
        Block.is_vaild_block(last_block, created_block)