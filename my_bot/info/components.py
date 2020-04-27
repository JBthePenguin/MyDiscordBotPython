from discord.ext.commands import Cog, command
from .config import COMPONENTS_COMMANDS as coms


class ComponentsCommands(Cog, name='Commands Info Components'):
    """ Class Category of commands to obtain infos for guild's components """

    def __init__(self, bot):
        self.bot = bot

    @command(name=coms.mem.name, help=coms.mem.help, ignore_extra=False)
    async def members(self, ctx, id_or_name):
        """ Send an embed with info for a specific member """
        # check parameter
        # parameter invalid -> send no member embed
        # parameter valid -> send embed with member's infos
        pass
