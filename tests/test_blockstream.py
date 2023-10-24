from tests.conftest import blockstream_provider


def test_get_block(blockstream_provider):
    block = blockstream_provider.get_block(0)
    assert (
        block["id"]
        == "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    )
