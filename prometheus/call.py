#!/usr/bin/python3

#TODO
# Implement subprocess (Priority: High)

from prometheus_client import start_http_server
import prometheus_client as prom
import time
import json

import os

PORT = 9000

BITCOIN_INTERFACE = "../umbrel/scripts/app compose bitcoin exec bitcoind bitcoin-cli"

#Metrics
BITCOIN_BLOCKS = prom.Gauge('bitcoin_blocks', 'Bitcoin blocks count')
BITCOIN_DIFFICULTY = prom.Gauge('blockchain_stats_difficulty', 'Bitcoin blockchain current difficulty')
BITCOIN_CONNECTIONS = prom.Gauge('bitcoin_core_connections', 'Connections to node')
LATEST_BLOCK_HASH = prom.Gauge('bitcoin_latest_block_hash', 'Latest block hash')

def request(command):
    request = BITCOIN_INTERFACE + " " + command
    run = os.popen(request)
    response = run.read()
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
        info = request("getblockhash" + str(blocks))
        LATEST_BLOCK_HASH.set(info)



        time.sleep(1)