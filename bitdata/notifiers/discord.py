from discordwebhook import Discord
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class DiscordWriter:
    def __init__(self):
        self.webhookurl = os.getenv("DISCORD_WEBHOOK_URL")
        self.discord = Discord(url = self.webhookurl)
       
    async def send_discord_message(self, message):
        self.discord.post(content=message)