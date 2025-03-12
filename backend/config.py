
"""configration file for aut adjuting the mining difficulty based on mining time"""
NANOSECONDS = 1
MICROSECONDS = 1000 * NANOSECONDS
MILLISECONDS = 1000 * MICROSECONDS
SECONDS = 1000 * MILLISECONDS

MINE_RATE = 4 * SECONDS

STARTING_BALANCE = 10000

MINE_REWARD =  250
MINE_REWARD_INPUT = { 'address': '*--mining--reward--*' }

print(MINE_REWARD)
