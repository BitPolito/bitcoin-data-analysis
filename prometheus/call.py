#!/usr/bin/python3
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
        BITCOIN_BLOCKS.set(info['blocks'])
        BITCOIN_DIFFICULTY.set(info['difficulty'])
        time.sleep(1)