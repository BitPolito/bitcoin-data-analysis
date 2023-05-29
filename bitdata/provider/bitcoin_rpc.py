from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from ..core.config import BitConfig
from loguru import logger
from tqdm import tqdm
from time import sleep

class BitcoinRPC:
    def __init__(self, cfg: BitConfig):
        self.cfg = cfg
        self.url = f"http://{cfg.RPC_USER}:{cfg.RPC_PASSWORD}@{cfg.RPC_HOST}:{str(cfg.RPC_PORT)}"
        self.rpc_conn = AuthServiceProxy(self.url, timeout=120)

    def get_block_by_height(self, height: int):
        # Get the block hash from the height
        try:
            block_hash = self.rpc_conn.getblockhash(height)
            logger.info(f"Getting block {block_hash} at height {height}")
        except JSONRPCException:
            logger.error(f"Block at height {height} not found")
            return None

        return self.rpc_conn.getblock(block_hash)

    def get_last_block_height(self):
        try:
            block_time = self.rpc_conn.getblockcount()
        except JSONRPCException:
            logger.error("Unable to get block height")
            return None

        logger.info(f"Getting last block height {block_time}")
        return block_time

    def get_transaction(self, txid: str):
        return self.rpc_conn.getrawtransaction(txid, True)

    def address_block_analytics(self, block: dict):
        # Create dictionaries to store the number and the amounts associated with each address type
        address_types_count = {}
        address_types_amount = {}

        for txid in tqdm(block["tx"]):
            tx = self.get_transaction(txid)
            for output in tx["vout"]:
                address_type = output["scriptPubKey"]["type"]
                address_types_count[address_type] = (
                    address_types_count.get(address_type, 0) + 1
                )
                address_types_amount[address_type] = (
                    address_types_amount.get(address_type, 0) + output["value"]
                )
            
        return {
            "address_types_count": address_types_count,
            "address_types_amount": address_types_amount,
        }
