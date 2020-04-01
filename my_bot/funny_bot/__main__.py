import os
from dotenv import load_dotenv
from bot_class import FunnyBot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if __name__ == "__main__":
    bot = FunnyBot()
    bot.run(TOKEN)
