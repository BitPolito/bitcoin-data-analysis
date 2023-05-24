from data_manager import DataManager
import time
import matplotlib.pyplot as plt

# Define the taproot activation height
taproot_activation_height = 709632


def taproot_analytics(data_manager: DataManager):

    # Initialize the plot
    fig, ax = plt.subplots()
    ax.set_xlabel("Block Height")
    ax.set_ylabel("Taproot Transactions")
    ax.set_title("Taproot Transactions Since Activation")

    # Start analyzing blocks between current_height and taproot_activation_height
    current_height = data_manager.get_last_block_height()

    for i in range(current_height, taproot_activation_height, -1):
        block = data_manager.get_block_by_height(i)
        tx_count = len(block["tx"])
        taproot_tx_count = 0
        for txid in block["tx"]:
            tx = data_manager.rpc_conn.getrawtransaction(txid, True)
            for output in tx["vout"]:
                if "taproot" in output["scriptPubKey"]["type"]:
                    taproot_tx_count += 1
                    break
        print(f"Block Height: {i}, Transactions: {tx_count}, Taproot Transactions: {taproot_tx_count}")
        ax.plot(i, taproot_tx_count, "bo")
        plt.draw()

        while True:
            # Check if a new blocks has been added to the blockchain
            new_height = data_manager.get_last_block_height()
            if new_height > current_height:
                # Analyze the new blocks
                for i in range(current_height + 1, new_height + 1):
                    block = data_manager.get_block_by_height(i)
                    tx_count = len(block["tx"])
                    taproot_tx_count = 0
                    for txid in block["tx"]:
                        tx = data_manager.rpc_conn.getrawtransaction(txid, True)
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