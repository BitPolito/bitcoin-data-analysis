### Extracting Data for the Last 10 Blocks

This Python script extracts data for the last 10 blocks of the Bitcoin blockchain using the 'bitcoinrpc' library and stores it in a pandas dataframe. The extracted data includes the following fields for each block:

-  Height
-  Timestamp
-   Transaction Count
-    BTC Fees
-    Size in MB
-    Branch ID
-    Coinbase Transaction
-    OP_RETURN

The script then maps the 'OP_RETURN' value to a specific mining operation and adds it to the block data before creating the pandas dataframe.

### Library and Methods Used
The following libraries ad methods are used in the script:

**AuthServiceProxy**

This is a class from the 'bitcoinrpc' library that provides an interface for communicating with a Bitcoin Core node via JSON-RPC. It takes three arguments:

    'rpc_user': The username for accessing the RPC interface of the Bitcoin Core node.
    'rpc_password': The password for accessing the RPC interface of the Bitcoin Core node.
    'rpc_ip': The IP address of the Bitcoin Core node.

Example usage:
```python
from bitcoinrpc.authproxy import AuthServiceProxy

rpc_user = 'bitcoin'
rpc_password = 'bitcoin'
rpc_port = '38333' #Signet portNumber
rpc_connection = AuthServiceProxy(
    f'http://{rpc_user}:{rpc_password}@localhost:{rpc_port}')
```


**getblockcount**

This method of the 'AuthServiceProxy' class returns the current block height of the Bitcoin blockchain.

Example usage:
```python
current_height = rpc_connection.getblockcount()
```


**getblockhash**

This method of the 'AuthServiceProxy' class takes a block height as an argument and returns the hash of the corresponding block.

Example usage:
```python
block_hash = rpc_connection.getblockhash(height)
```


**getblock**

This method of the AuthServiceProxy class takes a block hash as an argument and returns information about the corresponding block.

Example usage:
```python
block = rpc_connection.getblock(block_hash)
```


**getrawtransaction**

This method of the AuthServiceProxy class takes a transaction ID as an argument and returns information about the corresponding transaction.

Example usage:
```python
coinbase_tx = rpc_connection.getrawtransaction(block['tx'][0], 1)
```


**DataFrame**

This is a class from the pandas library that provides a data structure for storing tabular data in memory. It takes a dictionary of data and column labels as arguments.

Example usage:
```python
block_df = DataFrame(block_data)
```

**pandas.DataFrame.append**

This method of the DataFrame class appends rows to an existing dataframe. It takes a dictionary of data as an argument.

Example usage:
```python
block_df = block_df.append(block_data, ignore_index=True)
```

**pandas.DataFrame.apply**

This method of the DataFrame class applies a function to a dataframe or a column of a dataframe. It takes a function as an argument.

Example usage:
```python
block_df['Mining Operation'] = block_df['OP_RETURN'].apply(lambda x: mining_ops[x] if x in mining_ops else 'Unknown')
```


