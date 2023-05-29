import pytest

from bitdata.config import BitConfig
from bitdata.provider import BitcoinRPC, BlockstreamProvider


@pytest.fixture
def bitcoin_rpc():
    cfg = BitConfig()
    return BitcoinRPC(cfg)


@pytest.fixture
def blockstream_provider():
    return BlockstreamProvider()
