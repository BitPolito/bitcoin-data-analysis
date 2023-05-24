# bitcoin-data-analisys

This Python code allows for the analysis of taproot transactions on the Bitcoin blockchain. It uses the bitcoinrpc library to connect to a local Bitcoin node via RPC credentials, and then retrieves and analyzes block data to determine the number of taproot transactions. The code continuously runs in the background, checking for new blocks and updating the plot accordingly.

To use this code, a Bitcoin node running locally and RPC credentials set up are needed. bitcoinrpc and matplotlib libraries installed are necessary too.

The plot shows the number of taproot transactions on the y-axis and the block height on the x-axis. The plot updates in real-time as new blocks are added to the blockchain, showing the trend in taproot transactions over time.

Overall, this code provides a useful tool for analyzing the adoption and usage of taproot transactions on the Bitcoin blockchain.