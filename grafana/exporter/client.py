#!/usr/bin/python3

#TODO
# Implement subprocess                                                  (Priority: High) --> not needed if used BITCOIN_CLI = 0, fast enough
# Impelement signal handler (ex. ctlr+cv to exit process gratefully)    (Priority: Low)

from prometheus_client import start_http_server
import prometheus_client as prom
import time
import json

from bitcoin.rpc import Proxy
from typing import Union
from typing import Dict
from typing import Any
from typing import List
from btc_conf import *


import socket

import os

PORT = 9000
DEBUG = 0
BITCOIN_CLI = 0


BITCOIN_INTERFACE = "~/umbrel/scripts/app compose bitcoin exec bitcoind bitcoin-cli"

# Utilities
NUMBER_OF_REQUESTS = prom.Counter('Requests', 'Number of requesdts made to BTC container')
WARNINGS = prom.Counter("bitcoin_warnings", "Number of warning generated from btc node")
# BTC server info
SERVER_VERSION = prom.Gauge('bitcoin_server_info', 'Version of Bitcoin server')
PROTOCOL_VERSION = prom.Gauge('bitcoin_protocol_version', 'Bitcoin protocol number')
SIZE = prom.Gauge('size_on_disk', 'Blockchain size on disk')
UP_TIME = prom.Gauge('up_time', 'Server uptime value')
VERIFICATION_PROGRESS = prom.Gauge("verification_progress", "transaction's verification progress")

#Metrics
BLOCKS = prom.Gauge('bitcoin_blocks', 'Bitcoin blocks count')
PEERS = prom.Gauge('node_peers', 'Number of peers connected to the btc node')
DIFFICULTY = prom.Gauge('blockchain_stats_difficulty', 'Bitcoin blockchain current difficulty')
CONNECTION_IN = prom.Gauge('connections_in', 'connections in to node')
CONNECTION_OUT = prom.Gauge('connections_out', 'connections outgoing from node')
BAN_CREATED = prom.Gauge("ban_created", "Time the ban was created", labelnames=["address", "reason"])
BANNED_UNTIL = prom.Gauge("banned_until", "Time the ban expires", labelnames=["address", "reason"])
TXCOUNT = prom.Gauge('tx_count', 'total tx')
NUM_CHAINTIPS = prom.Gauge('num_chains', 'number of chains on the node') #different from each node, orphan chains are not sync so it depends on sync time
MEMINFO_USED = prom.Gauge("meminfo_used", "Number of bytes used")
MEMINFO_FREE = prom.Gauge("meminfo_free", "Number of bytes available")
MEMINFO_TOTAL = prom.Gauge("meminfo_total", "Number of bytes managed")
MEMINFO_LOCKED = prom.Gauge("meminfo_locked", "Number of bytes locked")
MEMINFO_CHUNKS_USED = prom.Gauge("meminfo_chunks_used", "Number of allocated chunks")
MEMINFO_CHUNKS_FREE = prom.Gauge("meminfo_chunks_free", "Number of unused chunks")

MEMPOOL_BYTES = prom.Gauge("mempool_bytes", "Size of mempool in bytes")
MEMPOOL_SIZE = prom.Gauge("mempool_size", "Number of unconfirmed transactions in mempool")
MEMPOOL_USAGE = prom.Gauge("mempool_usage", "Total memory usage for the mempool")
MEMPOOL_UNBROADCAST = prom.Gauge("mempool_unbroadcast", "Number of transactions waiting for acknowledgment")

TOTAL_BYTES_RECV = prom.Gauge("total_bytes_recv", "Total bytes received")
TOTAL_BYTES_SENT = prom.Gauge("total_bytes_sent", "Total bytes sent")


def rpc_client_slave():
    use_conf = ((CONF_PATH is not None) or (RPC_USER is None) or (RPC_PASSWORD is None))
    if use_conf:
        return lambda: Proxy(btc_conf_file=CONF_PATH, timeout=TIMEOUT)
    else:
        host = RPC_HOST
        host = "{}:{}@{}".format(RPC_USER, RPC_PASSWORD, host)
        if RPC_PORT:
            host = "{}:{}".format(host, RPC_PORT)
        service_url = "{}://{}".format(RPC_SCHEME, host)
        return lambda: Proxy(service_url=service_url, timeout=TIMEOUT)


def rpc_client_master():
    return rpc_client_slave()()


def bitcoinrpc(*args):
    result = rpc_client_master().call(*args)
    return result



def request(command):
    NUMBER_OF_REQUESTS.inc()
    if BITCOIN_CLI:
        request = BITCOIN_INTERFACE + " " + command
        run = os.popen(request)
        response = run.read()
        respons = json.loads(response)
    else:
        response = bitcoinrpc(command)
    return response




def tryPort(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("10.21.21.8", port))
        result = True
    except:
        print("Port is in use")
    sock.close()
    return result



if __name__ == '__main__':
    start_http_server(PORT)
    if DEBUG: 
        print("server started on port: " + str(PORT))
        print(tryPort(8332))
    while True:
        #Main object
        uptime = request("uptime")
        if DEBUG:
            print("uptime: ", uptime)
            print("\n")
        meminfo = request("getmemoryinfo")
        meminfo = meminfo["locked"]
        if DEBUG:
            print("meminfo: ", meminfo)
            print("\n")
        blockchaininfo = request("getblockchaininfo")
        if DEBUG:
            print("blockchaininfo: ", blockchaininfo)
            print("\n")
        networkinfo = request ("getnetworkinfo")
        if DEBUG:
            print("networkinfo: ", networkinfo)
            print("\n")
        chaintips = request("getchaintips")
        if DEBUG:
            print("chaintips: ", chaintips)
            print("\n")
        mempool = request("getmempoolinfo")
        if DEBUG:
            print("mempool: ",mempool)
            print("\n")
        nettotals = request("getnettotals")
        if DEBUG:
            print("nettotals: ", nettotals)
            print("\n")
        txstats = request("getchaintxstats")
        if DEBUG:
            print("txstats: ", txstats)
            print("\n")
        banned = request("listbanned") #Should be empty now :)
        if DEBUG:
            print("Banned: ", banned)
            print("\n")

        #Extract sub-object
        UP_TIME.set(int(uptime)) #Bitcoin node uptime (from last reboot)
        BLOCKS.set(blockchaininfo["blocks"])
        PEERS.set(networkinfo["connections"])
        if "connections_in" in networkinfo:
            CONNECTION_IN.set(networkinfo['connections_in'])
        if "connections_out" in networkinfo:
            CONNECTION_OUT.set(networkinfo['connections_out'])
        DIFFICULTY.set(blockchaininfo['difficulty'])

        SERVER_VERSION.set(networkinfo['version'])
        PROTOCOL_VERSION.set(networkinfo['protocolversion'])
        SIZE.set(blockchaininfo['size_on_disk'])
        VERIFICATION_PROGRESS.set(blockchaininfo['verificationprogress'])

        for Addban in banned:
            BAN_CREATED.labels(address=Addban["address"], reason=Addban.get("ban_reason", "manually added")).set(Addban["ban_created"])
            BANNED_UNTIL.labels(address=Addban["address"], reason=Addban.get("ban_reason", "manually added")).set(Addban["banned_until"])

        if networkinfo["warnings"]:
            WARNINGS.inc()

        TXCOUNT.set(txstats["txcount"])

        NUM_CHAINTIPS.set(len(chaintips))

        MEMINFO_USED.set(meminfo["used"])
        MEMINFO_FREE.set(meminfo["free"])
        MEMINFO_TOTAL.set(meminfo["total"])
        MEMINFO_LOCKED.set(meminfo["locked"])
        MEMINFO_CHUNKS_USED.set(meminfo["chunks_used"])
        MEMINFO_CHUNKS_FREE.set(meminfo["chunks_free"])

        MEMPOOL_BYTES.set(mempool["bytes"])
        MEMPOOL_SIZE.set(mempool["size"])
        MEMPOOL_USAGE.set(mempool["usage"])
        if "unbroadcastcount" in mempool:
            MEMPOOL_UNBROADCAST.set(mempool["unbroadcastcount"])

        TOTAL_BYTES_RECV.set(nettotals["totalbytesrecv"])
        TOTAL_BYTES_SENT.set(nettotals["totalbytessent"])

        time.sleep(10)