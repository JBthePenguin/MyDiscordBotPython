from discord.ext.commands import Cog


class ComponentsCommands(Cog, name='Commands Info Components'):
    """ Class Category of commands to obtain infos for guild's components """

    def __init__(self, bot):
        self.bot = bot
