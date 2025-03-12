from backend.utils.hasher import hasher


def test_hasher():
    """given diffrent order of iputs shloud return the same output"""
    assert hasher("hi", 8, [0]) == hasher(8, [0],"hi")
    assert hasher('foo') == 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'
