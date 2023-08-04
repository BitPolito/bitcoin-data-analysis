#!/usr/bin/python3

#TODO
# Implement subprocess                                                  (Priority: High)
# Impelement signal handler (ex. ctlr+cv to exit process gratefully)    (Priority: Low)

from prometheus_client import start_http_server
import prometheus_client as prom
import time
import json

import os

PORT = 9000

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
BAN_CREATED = prom.Gauge("bitcoin_ban_created", "Time the ban was created", labelnames=["address", "reason"])
BANNED_UNTIL = prom.Gauge("bitcoin_banned_until", "Time the ban expires", labelnames=["address", "reason"])
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

        #Main info object

        # uptime = int(bitcoinrpc("uptime"))
        # meminfo = bitcoinrpc("getmemoryinfo", "stats")["locked"]
        # blockchaininfo = bitcoinrpc("getblockchaininfo")
        # networkinfo = bitcoinrpc("getnetworkinfo")
        # chaintips = len(bitcoinrpc("getchaintips"))
        # mempool = bitcoinrpc("getmempoolinfo")
        # nettotals = bitcoinrpc("getnettotals")
        # rpcinfo = bitcoinrpc("getrpcinfo")
        # txstats = bitcoinrpc("getchaintxstats")

        uptime = request("uptime")
        print("uptime: ", uptime)
        print("\n")
        meminfo = request("getmemoryinfo")
        meminfo = meminfo["locked"]
        print("meminfo: ", meminfo)
        print("\n")
        blockchaininfo = request("getblockchaininfo")
        print("blockchaininfo: ", blockchaininfo)
        print("\n")
        networkinfo = request ("getnetworkinfo")
        print("networkinfo: ", networkinfo)
        print("\n")
        chaintips = request("getchaintips")
        print("chaintips: ", chaintips)
        print("\n")
        mempool = request("getmempoolinfo")
        print("mempool: ",mempool)
        print("\n")
        nettotals = request("getnettotals")
        print("nettotals: ", nettotals)
        print("\n")
        txstats = request("getchaintxstats")
        print("txstats: ", txstats)
        print("\n")
        banned = request("listbanned") #Should be empty now :)
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







        # network = request("getnetworkinfo")
        # SERVER_VERSION.set(network['version'])
        # PROTOCOL_VERSION.set(network['protocolversion'])

        # blockchain = request("getblockchaininfo")
        # #print(blockchain)
        # SIZE.set((blockchain['size_on_disk']/(1000*1000*1000))) #GigaBytes

        # UP_TIME.set(int(request("uptime")))

        # CHAIN_NUM.set(len(request("getchaintips")))

        # info = request("getrpcinfo")
        # print(info)

        
        # info = request("getmininginfo")
        # blocks = info['blocks']
        # BITCOIN_BLOCKS.set(blocks)
        # BITCOIN_DIFFICULTY.set(info['difficulty'])
        # info = request("getconnectioncount")
        # BITCOIN_CONNECTIONS.set(info)
        # #blocks = 799804
        # info = request("getblockhash " + str(blocks))
        # info = request("getblock " + latest_block_hash)
        # transactions = info['tx']
        # if blocks != block_number:
        #     #print(transactions[0])
        #     info = request("getrawtransaction " + str(transactions[0]))
        #     info = request("decoderawtransaction " + str(transactionId))
        #     print(info)
        # else:
        #     print("Already processed")


        # LATEST_BLOCK_NONCE.set(info['nonce'])
        # LATEST_BLOCK_TRANSACTIONS.set(info['nTx'])
        # LATEST_BLOCK_SIZE.set(info['size'])
        # print("Numero transazioni --> " + str(info['nTx']))
        #exit(0)
        # info = request("getrawtransaction 42ea59fcd6c686f165345bc441ce3ec0433fa7673342455772cdc5b882895277")
        # info = request("decoderawtransaction " + str(transactionId))
        # print(info)




        time.sleep(10)