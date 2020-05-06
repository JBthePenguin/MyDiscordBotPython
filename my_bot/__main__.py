from os import getenv
from sys import argv
from argparse import ArgumentParser
from dotenv import load_dotenv
from bot_class import MyBot

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

if __name__ == "__main__":
    if len(argv) == 1:  # no argument passed
        bot = MyBot()
    else:
        parser = ArgumentParser(
            description='\n'.join([
                'Run without argument for a bot with all commands, ',
                'or with optionnal one(s) for a bot with',
                ' only desired commands, or to run test', ]))
        parser.add_argument(
            '-i', '--info', action='store_true',
            help='Add InfoTeam commamds to the bot')
        parser.add_argument(
            '-e', '--event', action='store_true',
            help='Add Event commamds to the bot')
        args = parser.parse_args()
        bot = MyBot(info=args.info, event=args.event)
    bot.run(TOKEN)
