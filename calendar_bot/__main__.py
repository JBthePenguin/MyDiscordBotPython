import os
from dotenv import load_dotenv
from bot_class import CalendarBot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if __name__ == "__main__":
    bot = CalendarBot()
    bot.run(TOKEN)
