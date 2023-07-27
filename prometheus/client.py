#!/usr/bin/python3

#TODO
# Implement subprocess                                                  (Priority: High)
# Impelement signal handler (ex. ctlr+cv to exit process gratefully)    (Priority: Low)
# Metrics ideas:
# - avg fee for each block
# - total fee for each block (free from previous metric)
# - coinbase transaction --> who mined the block (pool, solo?)
# - tot BTC involved
# - list banned address

from prometheus_client import start_http_server
import prometheus_client as prom
import time
import json

import os

PORT = 9000

BITCOIN_INTERFACE = "~/umbrel/scripts/app compose bitcoin exec bitcoind bitcoin-cli"

#Utilities
NUMBER_OF_REQUESTS = prom.Counter('Requests', 'Number of requesdts made to BTC container')
#Metrics
BITCOIN_BLOCKS = prom.Gauge('bitcoin_blocks', 'Bitcoin blocks count')
BITCOIN_DIFFICULTY = prom.Gauge('blockchain_stats_difficulty', 'Bitcoin blockchain current difficulty')
BITCOIN_CONNECTIONS = prom.Gauge('bitcoin_core_connections', 'Connections to node')
LATEST_BLOCK_NONCE = prom.Gauge('bitcoin_latest_block_nonce', 'Latest block nonce')
LATEST_BLOCK_TRANSACTIONS = prom.Gauge('bitcoin_latest_block_transactions', 'Latest block transactions')
LATEST_BLOCK_SIZE = prom.Gauge('bitcoin_latest_block_size', 'Latest block size')


latest_block_hash = transactionId = block_transactions = block_number = 0
getblockhash_string = "getblockhash"
getrawtransaction_string = "getrawtransaction"

def request(command):
    NUMBER_OF_REQUESTS.inc()
    request = BITCOIN_INTERFACE + " " + command
    run = os.popen(request)
    response = run.read()
    #print(response)
    if getblockhash_string in command:
        global latest_block_hash
        latest_block_hash = response
        return 0
    elif getrawtransaction_string in command:
        global transactionId
        transactionId = response
        return 0
    else:
        return json.loads(response)

if __name__ == '__main__':
    start_http_server(PORT)
    print("server started on port: " + str(PORT))

    while True:
        info = request("getmininginfo")
        blocks = info['blocks']
        BITCOIN_BLOCKS.set(blocks)
        BITCOIN_DIFFICULTY.set(info['difficulty'])
        info = request("getconnectioncount")
        BITCOIN_CONNECTIONS.set(info)
        #blocks = 799804
        info = request("getblockhash " + str(blocks))
        info = request("getblock " + latest_block_hash)
        transactions = info['tx']
        if blocks != block_number:
            #print(transactions[0])
            info = request("getrawtransaction " + str(transactions[0]))
            info = request("decoderawtransaction " + str(transactionId))
            print(info)
        else:
            print("Already processed")


        LATEST_BLOCK_NONCE.set(info['nonce'])
        LATEST_BLOCK_TRANSACTIONS.set(info['nTx'])
        LATEST_BLOCK_SIZE.set(info['size'])
        print("Numero transazioni --> " + str(info['nTx']))
        exit(0)
        # info = request("getrawtransaction 42ea59fcd6c686f165345bc441ce3ec0433fa7673342455772cdc5b882895277")
        # info = request("decoderawtransaction " + str(transactionId))
        # print(info)




        time.sleep(1)