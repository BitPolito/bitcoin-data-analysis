#!/usr/bin/python3
import os
import time
import json

from prometheus_client import start_http_server, Gauge, Counter

#Easy way to extract data from node with bitcoin-cli
#not using bitcoin-cli command cuz in next umbrel version should be deprecated
#TODO
#1) Implement subprocess
#2) Format data to json
#3) Try to make some manipulation on data (avg between block mining?)

BITCOIN_INTERFACE = "../umbrel/scripts/app compose bitcoin exec bitcoind bitcoin-cli"

BITCOIN_BLOCKS = Gauge('bitcoin_blocks', 'Block height')

def request(command):
    request = BITCOIN_INTERFACE + " " + command
    run = os.popen(request)
    response = run.read()
    #print(response)
    return json.loads(response)

def main():
    start_http_server(9000)
    while True:
        info = request("getmininginfo")
        BITCOIN_BLOCKS.set(info['blocks'])
        print(info['blocks'])
        #request("getblockcount")
        #request("getdifficulty")
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        #print(test)

        #time.sleep(300)

if __name__ == '__main__':
    main()
