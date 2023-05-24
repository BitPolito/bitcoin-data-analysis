import time
from bitcoinrpc.authproxy import AuthServiceProxy
import matplotlib.pyplot as plt

# Connect to the BITPoliTO node using RPC credentials.
rpc_user = 'bitpolito'
rpc_password = 'bitpolito'
rpc_host = '127.0.0.1'
rpc_port = '8332'
rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_host, rpc_port), timeout=120)

# Define the taproot activation height
taproot_activation_height = 709632

# Initialize the plot
fig, ax = plt.subplots()
ax.set_xlabel("Block Height")
ax.set_ylabel("Taproot Transactions")
ax.set_title("Taproot Transactions Since Activation")

# Start analyzing blocks between current_height and taproot_activation_height
current_height = rpc_connection.getblockcount()

for i in range(current_height, taproot_activation_height, -1):
    block_hash = rpc_connection.getblockhash(i)
    block = rpc_connection.getblock(block_hash)
    tx_count = len(block["tx"])
    taproot_tx_count = 0
    for txid in block["tx"]:
        tx = rpc_connection.getrawtransaction(txid, True)
        for output in tx["vout"]:
            if "taproot" in output["scriptPubKey"]["type"]:
                taproot_tx_count += 1
                break
    print(f"Block Height: {i}, Transactions: {tx_count}, Taproot Transactions: {taproot_tx_count}")
    ax.plot(i, taproot_tx_count, "bo")
    plt.draw()

while True:
    # Check if a new blocks has been added to the blockchain
    new_height = rpc_connection.getblockcount()
    if new_height > current_height:
        # Analyze the new blocks
        for i in range(current_height + 1, new_height + 1):
            block_hash = rpc_connection.getblockhash(i)
            block = rpc_connection.getblock(block_hash)
            tx_count = len(block["tx"])
            taproot_tx_count = 0
            for txid in block["tx"]:
                tx = rpc_connection.getrawtransaction(txid, True)
                for output in tx["vout"]:
                    if "taproot" in output["scriptPubKey"]["type"]:
                        taproot_tx_count += 1
                        break
        print(f"Block Height: {new_height}, Transactions: {tx_count}, Taproot Transactions: {taproot_tx_count}")
        ax.plot(i, taproot_tx_count, "bo")
        plt.draw()
        plt.pause(0.001)
        current_height = new_height
    time.sleep(1)