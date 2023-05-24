from bitcoinrpc.authproxy import AuthServiceProxy

# Connect to the BITPoliTO node using RPC credentials.
rpc_user = 'bitpolito'
rpc_password = 'bitpolito'
rpc_host = '127.0.0.1'
rpc_port = '8332'
rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_host, rpc_port), timeout=120)

current_height = rpc_connection.getblockcount()
block_hash = rpc_connection.getblockhash(current_height)
block = rpc_connection.getblock(block_hash)
tx_count = len(block["tx"])

# Create dictionaries to store the number and the amounts associated with each address type
address_types_count = {}
address_types_amount = {}

for txid in block["tx"]:
    tx = rpc_connection.getrawtransaction(txid, True)
    for output in tx["vout"]:
        address_type = output["scriptPubKey"]["type"]
        address_types_count[address_type] = address_types_count.get(address_type, 0) + 1
        address_types_amount[address_type] = address_types_amount.get(address_type, 0) + output["value"]

# Print the results
print("Number of Transactions in Block " + str(current_height) + ": " + str(tx_count))
print("\nNumber of UTXOs by address type:")
for address_type, count in address_types_count.items():
    print(f"{address_type}: {count}")
    
print("\nAmount of UTXOs by address type:")
for address_type, amount in address_types_amount.items():
    print(f"{address_type}: {amount}")