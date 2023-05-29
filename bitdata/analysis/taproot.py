import time

import matplotlib.pyplot as plt
from ..provider.bitcoin_rpc import BitcoinRPC

# Define the taproot activation height
TAPROOT_ACTIVATION_HEIGHT = 709632

"""
This Python code allows for the analysis of taproot transactions on the Bitcoin blockchain. 
It uses the bitcoinrpc library to connect to a local Bitcoin node via RPC credentials, and then retrieves and analyzes block data to determine the number of taproot transactions. 
The code continuously runs in the background, checking for new blocks and updating the plot accordingly.
To use this code, a Bitcoin node running locally and RPC credentials set up are needed. bitcoinrpc and matplotlib libraries installed are necessary too.
The plot shows the number of taproot transactions on the y-axis and the block height on the x-axis. The plot updates in real-time as new blocks are added to the blockchain, showing the trend in taproot transactions over time.
Overall, this code provides a useful tool for analyzing the adoption and usage of taproot transactions on the Bitcoin blockchain.
"""


def taproot_counter(rpc_manager: BitcoinRPC):
    # Initialize the plot
    fig, ax = plt.subplots()
    ax.set_xlabel("Block Height")
    ax.set_ylabel("Taproot Transactions")
    ax.set_title("Taproot Transactions Since Activation")

    # Start analyzing blocks between current_height and taproot_activation_height
    current_height = rpc_manager.get_last_block_height()
    for i in range(current_height, TAPROOT_ACTIVATION_HEIGHT, -1):
        block = rpc_manager.get_block_by_height(i)
        tx_count = len(block["tx"])
        taproot_tx_count = 0
        for txid in block["tx"]:
            tx = rpc_manager.get_transaction(txid)
            for output in tx["vout"]:
                if "taproot" in output["scriptPubKey"]["type"]:
                    taproot_tx_count += 1
                    break
        print(
            f"Block Height: {i}, Transactions: {tx_count}, Taproot Transactions: {taproot_tx_count}"
        )
        ax.plot(i, taproot_tx_count, "bo")
        plt.draw()

        while True:
            # Check if a new blocks has been added to the blockchain
            new_height = rpc_manager.get_last_block_height()
            if new_height > current_height:
                # Analyze the new blocks
                for i in range(current_height + 1, new_height + 1):
                    block = rpc_manager.get_block_by_height(i)
                    tx_count = len(block["tx"])
                    taproot_tx_count = 0
                    for txid in block["tx"]:
                        tx = rpc_manager.get_transaction(txid)
                        for output in tx["vout"]:
                            if "taproot" in output["scriptPubKey"]["type"]:
                                taproot_tx_count += 1
                                break
                print(
                    f"Block Height: {new_height}, Transactions: {tx_count}, Taproot Transactions: {taproot_tx_count}"
                )
                ax.plot(i, taproot_tx_count, "bo")
                plt.draw()
                plt.pause(0.001)
                current_height = new_height
            time.sleep(1)


if __name__ == "__main__":
    from config import cfg

    rpc_manager = BitcoinRPC(cfg)
    taproot_counter(rpc_manager)
