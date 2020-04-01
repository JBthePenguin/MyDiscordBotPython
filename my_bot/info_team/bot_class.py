from os import getenv
from dotenv import load_dotenv
from discord.utils import get as get_obj
from discord.ext.commands import Bot
from commands import InfoCommands

load_dotenv()
GUILD = getenv('DISCORD_GUILD')


class InfoTeamBot(Bot):
    """ Custom Bot, subclass discord.ext.commands.Bot """

    def __init__(self):
        """ init discord.ext.commands.Bot
        and add custom proprieties and commands """
        super().__init__(command_prefix="!")
        # add commands and guild
        self.add_cog(InfoCommands(self))
        self.guild = ""

    def run(self, token):
        super().run(token)

    async def on_ready(self):
        """ print in console when bot is started and connected """
        self.guild = get_obj(self.guilds, name=GUILD)
        print('Info Team {} is connected to "{}"'.format(
            self.user, self.guild.name))

    async def on_command_error(self, ctx, error):
        """ send a message with the error """
        await ctx.send(str(error))