import requests


# Class that use the Blockstream API to get the blockchain data to do analysis


class BlockstreamProvider:

    def __init__(self):
        self.base_url = 'https://blockstream.info/api'

    def get_block(self, block_height):

        result = requests.get(f'{self.base_url}/block-height/{block_height}')
        return self.parse_result(result)

    def parse_result(self, result):    
        if result.status_code == 200:
            return result.json()
        else:
            return None
    
        
    def get_blockchain_info(self):

        result = requests.get(f'{self.base_url}/blocks/tip/height')

if __name__ == "__main__":

    bp = BlockstreamProvider()

    block = bp.get_block(0)

    print(block)

