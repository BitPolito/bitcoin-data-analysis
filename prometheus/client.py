#!/usr/bin/python3

#TODO
# Implement subprocess                                                  (Priority: High)
# Impelement signal handler (ex. ctlr+cv to exit process gratefully)    (Priority: Low)
# Metrics ideas:
# - avg fee for each block
# - total fee for each block (free from previous metric)
# - coinbase transaction --> who mined the block (pool, solo?)
# - tot BTC involved

from prometheus_client import start_http_server
import prometheus_client as prom
import time
import json

import os

PORT = 9000

BITCOIN_INTERFACE = "~/umbrel/scripts/app compose bitcoin exec bitcoind bitcoin-cli"

#Metrics
BITCOIN_BLOCKS = prom.Gauge('bitcoin_blocks', 'Bitcoin blocks count')
BITCOIN_DIFFICULTY = prom.Gauge('blockchain_stats_difficulty', 'Bitcoin blockchain current difficulty')
BITCOIN_CONNECTIONS = prom.Gauge('bitcoin_core_connections', 'Connections to node')
LATEST_BLOCK_NONCE = prom.Gauge('bitcoin_latest_block_nonce', 'Latest block nonce')
LATEST_BLOCK_TRANSACTIONS = prom.Gauge('bitcoin_latest_block_transactions', 'Latest block transactions')
LATEST_BLOCK_SIZE = prom.Gauge('bitcoin_latest_block_size', 'Latest block size')

latest_block_hash = 0
getblockhash_string = "getblockhash"

def request(command):
    request = BITCOIN_INTERFACE + " " + command
    run = os.popen(request)
    response = run.read()
    #print(response)
    if getblockhash_string in command:
        global latest_block_hash
        latest_block_hash = response
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
        blocks = 799804
        info = request("getblockhash " + str(blocks))
        info = request("getblock " + latest_block_hash)
        LATEST_BLOCK_NONCE.set(info['nonce'])
        LATEST_BLOCK_TRANSACTIONS.set(info['nTx'])
        LATEST_BLOCK_SIZE.set(info['size'])
        print(info['size'])





        time.sleep(1)
