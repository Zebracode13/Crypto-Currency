from backend.utils.hex_to_bin import hex_to_bin

def test_hex_to_bin():
    org = 420
    hex_num = hex(org)[2:]
    bin_org = hex_to_bin(hex_num)
    assert int(bin_org, 2) == org