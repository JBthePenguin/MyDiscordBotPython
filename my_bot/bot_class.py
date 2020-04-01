from os import getenv
from dotenv import load_dotenv
from discord.utils import get as get_obj
from discord.ext.commands import Bot
from tinydb import TinyDB
from info_team.commands import InfoCommands
from my_calendar.display_commands import EventDisplayCommands
from my_calendar.action_commands import EventActionCommands
from funny_bot.commands import FunnyCommands

load_dotenv()
GUILD = getenv("DISCORD_GUILD")


class FullBot(Bot):
    """ Custom Bot, subclass discord.ext.commands.Bot """

    def __init__(self):
        """ init discord.ext.commands.Bot and add custom commands """
        super().__init__(command_prefix="!")
        self.add_cog(InfoCommands(self))
        self.add_cog(EventDisplayCommands(self))
        self.add_cog(EventActionCommands(self))
        self.add_cog(FunnyCommands(self))
        self.guild = ""
        self.db = TinyDB("db.json")

    def run(self, token):
        super().run(token)

    async def on_ready(self):
        """ print in console when bot is started and connected """
        self.guild = get_obj(self.guilds, name=GUILD)
        print('Full {} is connected to "{}"'.format(
            self.user, self.guild.name))

    async def on_command_error(self, ctx, error):
        """ send a message with the error """
        await ctx.send(str(error))