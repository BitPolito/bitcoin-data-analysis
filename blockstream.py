import requests

# Class that use the Blockstream API to get the blockchain data to do analysis
class BlockstreamProvider:

    def __init__(self):
        self.base_url = 'https://blockstream.info/api'

    def get_block(self, block_height):
        result = requests.get(f'{self.base_url}/block-height/{block_height}')
        return self.parse_result(result)

    def get_blockchain_info(self):
        result = requests.get(f'{self.base_url}/blocks/tip/height')
        return self.parse_result(result)
    
    def parse_result(self, result):    
        if result.status_code == 200:
            return result.json()
        else:
            return None
    
        
    
if __name__ == "__main__":

    bp = BlockstreamProvider()

    block = bp.get_block(0)
    print(block)

    blockchain_info = bp.get_blockchain_info()
    print(blockchain_info)

