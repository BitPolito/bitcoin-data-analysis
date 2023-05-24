from config import Settings
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


class BitcoinRPC:
    def __init__(self, cfg: Settings):
        self.cfg = cfg
        self.url = f"http://{cfg.RPC_USER}:{cfg.RPC_PASSWORD}@{cfg.RPC_HOST}:{str(cfg.RPC_PORT)}" 
        self.rpc_conn = AuthServiceProxy(self.url, timeout=120)

    def get_block_by_height(self, height: int):
        # Get the block hash from the height
        block_hash = self.rpc_conn.getblockhash(height) 
        return self.rpc_conn.getblock(block_hash)

    def get_last_block_height(self):
        return self.rpc_conn.getblockcount()
        
    def address_block_analytics(self, block: dict):
        # Create dictionaries to store the number and the amounts associated with each address type
        address_types_count = {}
        address_types_amount = {}

        for txid in block["tx"]:
            tx = self.rpc_conn.getrawtransaction(txid, True)
            for output in tx["vout"]:
                address_type = output["scriptPubKey"]["type"]
                address_types_count[address_type] = address_types_count.get(address_type, 0) + 1
                address_types_amount[address_type] = address_types_amount.get(address_type, 0) + output["value"]
        return {
            "address_types_count": address_types_count,
            "address_types_amount": address_types_amount
        }

                