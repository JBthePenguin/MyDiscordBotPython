from discord.ext.commands import Bot
# from tinydb import TinyDB
from info_team.commands import InfoCommands
# from my_calendar.display_commands import EventDisplayCommands
# from my_calendar.action_commands import EventActionCommands


class MyBot(Bot):
    """ Custom Bot, subclass discord.ext.commands.Bot """

    def __init__(self, info=True, event=True):
        """ init discord.ext.commands.Bot and add desired commands """
        super().__init__(command_prefix="#")
        self.label = '- '
        if info is True:  # add Info team commands
            self.add_cog(InfoCommands(self))
            self.label += 'Info Team - '
        if event is True:  # add Event commands
            # self.add_cog(EventDisplayCommands(self))
            # self.add_cog(EventActionCommands(self))
            # self.db = TinyDB("db.json")
            self.label += 'Event - '

    def run(self, token):
        super().run(token)

    async def on_ready(self):
        """ print in shell when bot is connected to guilds """
        guild_names = []
        for guid in self.guilds:
            guild_names.append(guid.name)
        print('{} {} is connected to "{}"'.format(
            self.label, self.user.name, ' - '.join(guild_names)))

    async def on_command_error(self, ctx, error):
        """ send a message with the error """
        await ctx.send(str(error))
