import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode

load_dotenv()  # take environment variables from .env.


class TelegramWriter:
    def __init__(
        self,
    ):
        self._token = os.getenv("BOT_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")
        self.bot = Bot(token=self._token)

    async def send_telegram_message(self, message):
        if self.bot:
            await self.bot.send_message(
                chat_id=self.chat_id, text=message, parse_mode=ParseMode.MARKDOWN_V2
            )
