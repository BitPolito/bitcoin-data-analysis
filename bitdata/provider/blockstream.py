import requests
# Class that use the Blockstream API to get the blockchain data to do analysis
class BlockstreamProvider:
    def __init__(self, network="mainnet"):
        self.network = network
        if network == "testnet":
            self.base_url = "https://blockstream.info/testnet/api"
        else:
            self.base_url = "https://blockstream.info/api"

    def get_block(self, block_height):
        return requests.get(f"{self.base_url}/block-height/{block_height}").text

    def get_last_height(self):
        return requests.get(f"{self.base_url}/blocks/tip/height").text
    
    def last_hash(self):
        return requests.get(f"{self.base_url}/blocks/tip/hash").text

    def get_last_n_blocks(self, n=10):
        result = requests.get(f"{self.base_url}/blocks/:{n}")
        print(f"{self.base_url}/blocks/:{n}")
        return self.parse_result(result)
    

    def get_raw_coinbase_transaction(self, block_hash: str = ""):
        coinbase_transaction_hash = requests.get(f"{self.base_url}/block/{block_hash}/txid/0").text
        coinbase_transaction_raw = requests.get(f"{self.base_url}/tx/{coinbase_transaction_hash}/raw").text
        return coinbase_transaction_raw

    def parse_result(self, result):
        if result.status_code == 200:
            return result.json()
        else:
            return None


if __name__ == "__main__":
    print("BlockstreamProvider")
    # bp = BlockstreamProvider()

    # block = bp.get_block(0)
    # print(block)

    # blockchain_info = bp.get_blockchain_info()
    # print(blockchain_info)
