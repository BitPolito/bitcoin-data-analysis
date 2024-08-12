import time
import requests
from pydantic import BaseModel


class LightningStats(BaseModel):
    id: int
    added: str
    channel_count: int
    node_count: int
    total_capacity: int
    tor_nodes: int
    clearnet_nodes: int
    unannounced_nodes: int
    avg_capacity: int
    avg_fee_rate: int
    avg_base_fee_mtokens: int
    med_capacity: int
    med_fee_rate: int
    med_base_fee_mtokens: int
    clearnet_tor_nodes: int


class MempoolProvider:
    def __init__(self, network="mainnet") -> None:
        self.network = network
        if network == "testnet4":
            self.base_url = "https://mempool.space/testnet4/api"
        else:
            self.base_url = "https://mempool.space/api"

    def get_block_hash(self, block_height):
        """Fetches block hash by height."""
        response = requests.get(f"{self.base_url}/block-height/{block_height}")
        return response.text.strip()

    def get_block(self, block_hash):
        """Fetches block data by hash and returns it as a dictionary."""
        response = requests.get(f"{self.base_url}/block/{block_hash}")
        return self.parse_result(response)

    def get_last_height(self):
        """Fetches the height of the latest block."""
        response = requests.get(f"{self.base_url}/blocks/tip/height")
        return int(response.text.strip())

    def last_hash(self):
        """Fetches the hash of the latest block."""
        response = requests.get(f"{self.base_url}/blocks/tip/hash")
        return response.text.strip()

    def get_last_n_blocks(self, n=10):
        """Fetches the last n blocks."""
        latest_height = self.get_last_height()
        start_height = max(0, latest_height - n + 1)
        blocks = []
        for height in range(start_height, latest_height + 1):
            block_hash = self.get_block_hash(height)
            print(block_hash)
            time.sleep(1)
            block = self.get_block(block_hash)
            if block:
                blocks.append(block)
        return blocks

    def get_raw_coinbase_transaction(self, block_hash: str = ""):
        """Fetches the raw coinbase transaction from a given block hash."""
        coinbase_transaction_hash = requests.get(
            f"{self.base_url}/block/{block_hash}/txid/0"
        ).text
        coinbase_transaction_raw = requests.get(
            f"{self.base_url}/tx/{coinbase_transaction_hash}/raw"
        ).text
        return coinbase_transaction_raw

    def get_block_by_hash(self, block_hash):
        """Fetches block data by hash."""
        response = requests.get(f"{self.base_url}/block/{block_hash}")
        return self.parse_result(response)

    def get_lightning_stats(self):
        """Returns network-wide stats such as total number of channels and nodes, total capacity, and average/median fee figures."""
        url = f"{self.base_url}/v1/lightning/statistics/latest"
        response = requests.get(url)
        result = self.parse_result(response)
        if not result:
            return None

        stats = result.get("latest", None)
        if not stats:
            return None

        try:
            return LightningStats(**stats)
        except Exception as e:
            print(e)
            return stats

    def parse_result(self, response):
        """Parses HTTP response into JSON if status code is 200."""
        if response.status_code == 200:
            return response.json()
        else:
            return None


if __name__ == "__main__":
    mempool = MempoolProvider()

    # Example usage of the new methods
    block_height = 0
    print("Block at height", block_height, ":", mempool.get_block(block_height))
    print("Latest block height:", mempool.get_last_height())
    print("Latest block hash:", mempool.last_hash())
    print("Last 10 blocks:", mempool.get_last_n_blocks(10))

    block_hash = mempool.last_hash()
    print("Raw coinbase transaction from block hash", block_hash, ":", mempool.get_raw_coinbase_transaction(block_hash))

    stats = mempool.get_lightning_stats()
    print("Lightning network stats:", stats)
