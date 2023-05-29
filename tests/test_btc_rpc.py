from tests.conftest import bitcoin_rpc


def test_last_block_height(bitcoin_rpc):
    last_block_height = bitcoin_rpc.get_last_block_height()
    assert last_block_height is not None
    assert isinstance(last_block_height, int)
    assert last_block_height > 0
