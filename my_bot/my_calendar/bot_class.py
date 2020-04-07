from discord.ext.commands import Bot
from tinydb import TinyDB
from display_commands import EventDisplayCommands
from action_commands import EventActionCommands


class CalendarBot(Bot):
    """ Custom Bot, subclass discord.ext.commands.Bot """

    def __init__(self):
        """ init discord.ext.commands.Bot
        and add custom proprieties and commands """
        super().__init__(command_prefix="#")
        # add commands and json db
        self.add_cog(EventDisplayCommands(self))
        self.add_cog(EventActionCommands(self))
        self.db = TinyDB("db.json")

    def run(self, token):
        super().run(token)

    async def on_ready(self):
        """ print in shell when bot is connected to guilds """
        guild_names = []
        for guid in self.guilds:
            guild_names.append(guid.name)
        print('Calendar {} is connected to "{}"'.format(
            self.user.name, ' - '.join(guild_names)))

    async def on_command_error(self, ctx, error):
        """ send a message with the error """
        await ctx.send(str(error))
