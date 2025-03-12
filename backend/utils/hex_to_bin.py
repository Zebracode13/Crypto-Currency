from backend.utils.hasher import hasher

HEX_TO_BINARY_TABLE = {
    '0':'0000',
    '1':'0001',
    '2':'0010',
    '3':'0011',
    '4':'0100',
    '5':'0101',
    '6':'0110',
    '7':'0111',
    '8':'1000',
    '9':'1001',
    'a':'1010',
    'b':'1011',
    'c':'1100',
    'd':'1101',
    'e':'1110',
    'f':'1111',
}

def hex_to_bin(hex_str):
    """Coverts Hex to Binary"""
    bin_str = ''
    for char in hex_str:
        bin_str += HEX_TO_BINARY_TABLE[char]
    return bin_str



def main():
    """Runs file"""
    val = 420

    hex_val = hex(val)[2:]
    print(hex_val)

    bin_num = hex_to_bin(hex_val)
    print(bin_num)

    real_num_val = int(bin_num, 2)
    print(real_num_val)

    crypto_hashed = hex_to_bin(hasher(420))
    print(crypto_hashed)

if __name__ == '__main__':
    main()