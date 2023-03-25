from bitcoinrpc.authproxy import AuthServiceProxy
from pandas import DataFrame

# Connect to the Bitpoloito node using RPC credentials.
rpc_user = 'bitcoin'
rpc_password = 'bitcoin'
rpc_port = '38333'
rpc_connection = AuthServiceProxy(
    f'http://{rpc_user}:{rpc_password}@localhost:{rpc_port}')

# Iterate over the last 10 blocks and extract the required data.
block_data = []
current_height = rpc_connection.getblockcount()

for height in range(current_height, current_height - 10, -1):
    # Get the block hash and information for the current height.
    block_hash = rpc_connection.getblockhash(height)
    block = rpc_connection.getblock(block_hash)

    # Get the coinbase transaction for the block.
    coinbase_tx = rpc_connection.getrawtransaction(block['tx'][0], 1)

    # Extract the value of the OP_RETURN output from the coinbase transaction for the block.
    op_return_value = None

    for output in coinbase_tx['vout']:
        if output['scriptPubKey']['type'] == 'nulldata':
            op_return_value = output['scriptPubKey']['asm'].split(' ')[1]
            break

    # Add the block data to the block data list.
    block_data.append({
        'Height': height,
        'Timestamp': block['time'],
        'Transaction Count': len(block['tx']),
        'BTC Fees': block['fee'],
        'Size (MB)': block['size'] / 1000000,
        'Branch ID': 'Orphan' if block['confirmations'] == 0 else 'Main',
        'Coinbase Transaction': coinbase_tx,
        'OP_RETURN': op_return_value
    })

# Map the OP_RETURN value to the mining operation and add it to the pandas dataframe.
mining_ops = {
    '54686520496e7465726e65746f662042697420426f6e6473': 'Unknown',
    '5765622050726f766f736b79': 'Web Provosky',
    '416c6978612054726164696e67205465726d': 'Alexa Trading',
    '4d696e656420426974636f696e': 'Mined Bitcoin',
    '4e6f746172696f757320434f564944': 'Notarious COVID',
    '496e66696e69747950726f6d6f74696f6e': 'InfinityPromotion',
    '466f726d756c61205465726d': 'FormulaTerm',
    '4269746d696e657273206f662046756c6c466f726365': 'FullForce',
    '44696769626f7920426974636f696e': 'Digibyte Pool',
    '426974486f6c6520486f6c64696e67': 'BitHole Holding',
    '4c696768746e696e6720526f636b73': 'Lightning Rocks',
    '52696768674d696e656420416c6c69616e6365': 'RightMining Alliance',
    # '50696f6e657820576f726b73': 'Pionex',
    # '4269747374616d70': 'Bitstamp',
    '536c75736820506f6f6c': 'Slush Pool',
    '4632506f6f6c': 'F2Pool',
    '416e74706f6f6c': 'Antpool',
    '566961425463': 'ViaBTC',
    '4254632e636f6d': 'BTC.com',
    '506f6f6c696e': 'Poolin',
    '47656e65736973204d696e696e67': 'Genesis Mining',
    '42697466757279': 'Bitfury',
    '42696e616e636520506f6f6c': 'Binance Pool',
    '4b616e6f20506f6f6c': 'Kano Pool',
    '636f696e62617365': 'Coinbase',
    '4254432d474c': 'BTCC Pool',
    '456c6967697573': 'Eligius',
    '4b616e6f': 'KanoPool',
    '5761746572746578': 'Waterhole',
}

for block in block_data:
    op_return_value = block['OP_RETURN']
    if op_return_value in mining_ops:
        block['Mining Operation'] = mining_ops[op_return_value]
    else:
        block['Mining Operation'] = 'Unknown'

# Create a pandas dataframe with the block data.
block_df = DataFrame(block_data)

# Print the resulting dataframe.
print(block_df)
