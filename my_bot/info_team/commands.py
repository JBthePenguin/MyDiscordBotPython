from discord.ext.commands import Cog, command
from discord.utils import get as get_obj


class InfoCommand(Cog, name='Commandes pour lister des infos'):

    def __init__(self, bot):
        self.bot = bot

    # without params
    @command(
        name='list_membres',
        help='liste tous les membres -> !list_membres')
    async def list_members(self, ctx):
        """ send a message with the list of all members """
        members = '\n - '.join(
            [member.name for member in self.bot.guild.members])
        message = 'Membres de {}:\n - {}'.format(
            self.bot.guild.name, members)
        await ctx.send(message)

    @command(
        name='list_roles',
        help='liste les différents rôles-> !list_roles')
    async def list_roles(self, ctx):
        """ send a message with the list of roles """
        roles = '\n - '.join([role.name for role in self.bot.guild.roles])
        message = 'Rôles de {}:\n - {}'.format(
            self.bot.guild.name, roles)
        await ctx.send(message)

    @command(
        name='list_salons',
        help='liste tous les salons par catégorie-> !list_salons')
    async def list_salons(self, ctx):
        """ send a message with the list of channels by category """
        categories = self.bot.guild.by_category()
        messages = []
        for category in categories:
            channels = '\n - '.join([channel.name for channel in category[1]])
            messages.append('{}:\n - {}'.format(category[0].name, channels))
        for message in messages:
            await ctx.send(message)

    # with params
    @command(
        name='list_membres_role',
        help='liste les membres d un rôle-> !list_membres_role "role"')
    async def list_membres_role(self, ctx, role_name):
        """ send a message with the list of members for a specific role """
        # get role
        role = get_obj(self.bot.guild.roles, name=role_name)
        if role is None:
            # no role with this name
            message = 'Pas de rôle "{}"'.format(role_name)
        else:
            role_members = []
            for member in self.bot.guild.members:
                if role in member.roles:
                    role_members.append(member)
            if role_members == []:
                message = 'Aucun membre avec le rôle "{}""'.format(role_name)
            else:
                members = '\n - '.join(
                    [member.name for member in role_members])
                message = '{}\n - {}'.format(role_name, members)
        await ctx.send(message)

    @command(
        name='list_membres_salon',
        help='liste les membres d un salon-> !list_membres_salon "salon"')
    async def list_membres_salon(self, ctx, channel_name):
        """ send a message with the list of members
        who have permission for a channel"""
        # get channel
        channel = get_obj(self.bot.guild.channels, name=channel_name)
        if channel is None:
            # no channel with this name
            message = 'Pas de salon {}'.format(channel_name)
        else:
            # list authorized members
            auth_members = []
            for member in self.bot.guild.members:
                permissions = channel.permissions_for(member)
                if permissions.view_channel:
                    auth_members.append(member)
            if auth_members == []:
                message = 'Aucun membre autorisé pour le salon {}'.format(
                    channel_name)
            else:
                members = '\n - '.join(
                    [member.name for member in auth_members])
                message = '{}\n - {}'.format(channel_name, members)
        await ctx.send(message)
