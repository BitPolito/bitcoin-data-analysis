from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import pandas as pd
import base64
from bitcoin_rpc import BitcoinRPC


# Create a DataFrame

df_blocks = pd.DataFrame(columns=['Height', 'OP_RETURN', 'Timestamp', 'Transaction count', 'BTC fees', 'Size in MB'])

# Iterate over each block
for block_height in range(rpc_connection.getblockcount() - 100, rpc_connection.getblockcount()):
    try:
        block_hash = rpc_connection.getblockhash(block_height)
        block = rpc_connection.getblock(block_hash)
        
        # Extract the coinbase transaction
        coinbase_txid = block['tx'][0]
        coinbase_tx = rpc_connection.getrawtransaction(coinbase_txid, 1)
        
        # Extract the mining tag 
        coinbase_vin = coinbase_tx['vin'][0]['coinbase']
        # Decode the mining tag
        coinbase_text = bytes.fromhex(coinbase_vin).decode('utf-8')
        # Extract block information
        block_info = {
            'Height': block_height,
            'Coinbase Test': coinbase_text,
            'Timestamp': block['time'],
            'Transaction count': block['nTx'],
            'BTC fees': block.get('fee', 0),
            'Size in MB': block['size']/1024/1024
        }
        
        # Add the information to the DataFrame
        df_blocks = df_blocks.append(block_info, ignore_index=True)
        
    except Exception as e:
        print(f'Error: {e}')

# Mapping between OP_RETURN value and mining pool
op_return_mapping = {
    '636f696e62617365': 'Coinbase',
    '736c757368': 'Slush Pool',
    '4254432d474c': 'BTCC Pool',
    '616e74506f6f6c': 'AntPool',
    '456c6967697573': 'Eligius',
    '4b616e6f': 'KanoPool',
    '5761746572746578': 'Waterhole'
}

print(df_blocks)
