"""Offline migration checks; never connect to Bitcoin RPC, Telegram or public APIs."""
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch


class DependencyCompatibilityTests(unittest.TestCase):
    def test_settings_and_rpc_client(self):
        from bitdata.core.config import BitConfig
        from bitdata.provider.bitcoin_rpc import BitcoinRPC

        config = BitConfig(_env_file=None, RPC_USER="fixture", RPC_PASSWORD="fixture",
                           RPC_HOST="127.0.0.1", RPC_PORT=18443)
        client = Mock()
        client.getblockcount.return_value = 100
        client.getblockhash.return_value = "fixture-block"
        client.getblock.return_value = {"tx": []}
        with patch("bitdata.provider.bitcoin_rpc.AuthServiceProxy", return_value=client):
            provider = BitcoinRPC(config)
            self.assertEqual(provider.get_last_block_height(), 100)
            self.assertEqual(provider.get_block_by_height(100), {"tx": []})

    def test_http_provider(self):
        from bitdata.provider.mempool import MempoolProvider

        response = Mock(status_code=200)
        response.json.return_value = {"id": "fixture-block", "height": 100}
        with patch("bitdata.provider.mempool.requests.get", return_value=response) as get:
            result = MempoolProvider(network="testnet4").get_block("fixture-block")
        self.assertEqual(result["height"], 100)
        get.assert_called_once_with("https://mempool.space/testnet4/api/block/fixture-block")

    def test_dataframe_arrow_plot_and_logo(self):
        import pandas as pd
        import pyarrow as pa
        import plotly.express as px
        import streamlit
        from PIL import Image

        frame = pd.DataFrame({"height": [1, 2], "transactions": [10, 20]})
        self.assertEqual(pa.Table.from_pandas(frame).num_rows, 2)
        self.assertEqual(len(px.line(frame, x="height", y="transactions").data), 1)
        self.assertTrue(callable(streamlit.plotly_chart))
        with Image.open(Path(__file__).parent / "dashboard/bitpolito_logo.png") as image:
            image.load()
            self.assertGreater(image.width, 0)


class TelegramCompatibilityTests(unittest.IsolatedAsyncioTestCase):
    async def test_notification_awaits_the_telegram_client(self):
        from bitdata.notifiers.telegram import TelegramWriter

        bot = Mock(send_message=AsyncMock())
        with patch.dict("os.environ", {"BOT_TOKEN": "fixture", "CHAT_ID": "fixture"}), \
                patch("bitdata.notifiers.telegram.Bot", return_value=bot):
            writer = TelegramWriter()
            await writer.send_telegram_message("public fixture")
        bot.send_message.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
