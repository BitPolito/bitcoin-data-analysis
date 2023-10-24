import argparse
import asyncio

from bitdata.notifiers.telegram import TelegramWriter
from bitdata.provider.blockstream import BlockstreamProvider

# This script will listen for new blocks and check if the coinbase transaction contains the string "Stratum v2"
# If it does, it will send a message to the Telegram channel
# The raw transaction converted in text contains also the miner input (?)

SLEEP_TIME = 30  # Time to wait in seconds between checks


class CoinbaseAnalyzer:
    def __init__(
        self,
        provider,
        telegram_writer,
        target_string,
        network="testnet",
        n_previous_blocks=0,
    ):
        self.provider = provider
        self.telegram_writer = telegram_writer
        self.target_string = target_string
        self.last_hash = None
        self.network = network
        self.n_previous_blocks = n_previous_blocks

    def get_miner_text_input(self, raw_transaction):
        try:
            inputs = raw_transaction["result"]["vin"]
            script = inputs[0]["coinbase"]
            ascii_string = ""
            for i in range(0, len(script), 2):
                ascii_string += chr(int(script[i : i + 2], 16))
            return ascii_string.lower()
        except Exception as e:
            # The raw transaction as string may contain the miner input
            return raw_transaction.lower()

    async def notify_message(self, block_height, block_hash):
        url = (
            "https://mempool.space/it/testnet/block/"
            if self.network == "testnet"
            else "https://mempool.space/it/block/"
        )
        message = f"""Found target string: **{self.target_string}** in {self.network} Block: [@{block_height}]({url}{block_hash})"""
        await self.telegram_writer.send_telegram_message(message)

    async def check_new_block(self):
        last_hash = self.provider.last_hash()
        if last_hash == self.last_hash:
            return
        self.last_hash = last_hash
        # New block found
        last_height = self.provider.get_last_height()
        coinbase_raw_transaction = self.provider.get_raw_coinbase_transaction(last_hash)
        miner_input = self.get_miner_text_input(coinbase_raw_transaction)
        if self.target_string.lower() in miner_input:
            await self.notify_message(last_height, last_hash)
        else:
            print(f"New block: {last_height} - {self.last_hash}")

    async def check_from_previous_n_blocks(self):
        if self.n_previous_blocks <= 0:
            return
        list_of_blocks = self.provider.get_last_n_blocks(self.n_previous_blocks)
        for block in list_of_blocks[: self.n_previous_blocks]:
            block_hash = block["id"]
            block_height = block["height"]
            coinbase_raw_transaction = self.provider.get_raw_coinbase_transaction(
                block_hash
            )
            miner_input = self.get_miner_text_input(coinbase_raw_transaction)
            if self.target_string.lower() in miner_input:
                await self.notify_message(block_height, block_hash)

    async def run(self):
        await self.check_from_previous_n_blocks()
        while True:
            await self.check_new_block()
            await asyncio.sleep(SLEEP_TIME)  # Wait for 10 seconds before checking again


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Block Analyzer Script")
    parser.add_argument(
        "--network",
        "-n",
        type=str,
        default="testnet",
        help="Network (e.g., testnet or mainnet)",
    )
    parser.add_argument(
        "--target",
        "-t",
        type=str,
        default="stratum v2",
        help="Target string to search in miner input",
    )
    parser.add_argument(
        "--previous",
        "-p",
        type=int,
        default=0,
        help="Number of previous blocks to check from",
    )
    args = parser.parse_args()

    network = args.network
    target_string = args.target
    n_previous_blocks = args.previous
    provider = BlockstreamProvider(network=network)
    telegram_writer = TelegramWriter()
    coinbase_analyzer = CoinbaseAnalyzer(
        provider, telegram_writer, target_string, network, n_previous_blocks
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coinbase_analyzer.run())
