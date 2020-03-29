from discord.ext.commands import Cog, command


class InfoCommand(Cog, name='Commandes pour lister des infos'):

    def __init__(self, bot):
        self.bot = bot

    @command(
        name='list_membres',
        help='liste de tous les membres de la guilde.')
    async def list_members(self, ctx):
        """ send a message with the list of all members """
        members = '\n - '.join(
            [member.name for member in self.bot.get_guild().members])
        message = 'Membres de {}:\n - {}'.format(
            self.bot.get_guild().name, members)
        await ctx.send(message)

    @command(
        name='list_roles',
        help='liste les différents rôles de la guilde.')
    async def list_roles(self, ctx):
        """ send a message with the list of roles """
        roles = '\n - '.join([role.name for role in self.bot.get_guild().roles])
        message = 'Rôles de {}:\n - {}'.format(
            self.bot.get_guild().name, roles)
        await ctx.send(message)
