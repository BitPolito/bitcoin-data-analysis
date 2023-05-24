from bitcoin_rpc import BitcoinRPC


def last_block_analytics(rpc_manager: BitcoinRPC):

    current_height = rpc_manager.get_last_block_height()
    last_block = rpc_manager.get_block_by_height(current_height)
    tx_count = len(last_block["tx"])

    address_result = rpc_manager.address_block_analytics(last_block)
    address_types_count = address_result["address_types_count"]
    address_types_amount = address_result["address_types_amount"]

    # Print the results
    print("Number of Transactions in Block " + str(current_height) + ": " + str(tx_count))
    print("\nNumber of UTXOs by address type:")
    for address_type, count in address_types_count.items():
        print(f"{address_type}: {count}")

    print("\nAmount of UTXOs by address type:")
    for address_type, amount in address_types_amount.items():
        print(f"{address_type}: {amount}")


if __name__ == "__main__":
    from config import cfg 
    rpc_manager = BitcoinRPC(cfg)
    last_block_analytics(rpc_manager)