from discord.ext.commands import Cog, command
from discord.utils import get as get_obj

# Configurations of commands -> [[name, help], [name, help], ...]
confs = [
    ['membres', 'Tous les membres-> !membres'],
    ['roles', 'Tous les rôles-> !roles'],
    ['salons', 'Tous les salons par catégorie-> !salons'],
    ['membres_role', 'Les membres du rôle-> !membres_role "nom du role"'],
    ['membres_salon', 'Les membres du salon-> !membres_salon "nom du salon"']]


class InfoCommands(Cog, name='Commandes Info'):

    def __init__(self, bot):
        self.bot = bot

    def format_message(self, title, list_obj):
        """ return a formated message with a list of object's name """
        list_obj_formated = '\n - '.join(
            [obj.name for obj in list_obj])
        return '{}:\n - {}'.format(title, list_obj_formated)

    def check_param(self, list_obj, obj_name):
        """ Check if parameter is Ok, return the corresponding object if it is
        or a none message if not """
        obj = get_obj(list_obj, name=obj_name)
        if obj is None:
            # no role with this name
            return '"{}" introuvable'.format(obj_name)
        else:
            return obj

    def add_condition(self, list_members, member_checked, add_conditon):
        """ check if the condition is True
        and add member to the list if it's ok """
        if add_conditon is True:
            list_members.append(member_checked)

    def check_empty_list(self, title, list_members):
        """ return no members if list is empty
        or a formated message with it if not """
        if list_members == []:
            return 'Aucun membre trouvé'
        return self.format_message(title, list_members)

    # commands without params
    @command(name=confs[0][0], help=confs[0][1], ignore_extra=False)
    async def list_members(self, ctx):
        """ send a message with the list of all members """
        await ctx.send(self.format_message(
            'Membres de {}'.format(self.bot.guild.name),
            self.bot.guild.members))

    @command(name=confs[1][0], help=confs[1][1], ignore_extra=False)
    async def list_roles(self, ctx):
        """ send a message with the list of roles """
        await ctx.send(self.format_message(
            'Rôles de {}'.format(self.bot.guild.name),
            self.bot.guild.roles))

    @command(name=confs[2][0], help=confs[2][1], ignore_extra=False)
    async def list_salons(self, ctx):
        """ send a message with the list of channels for each category """
        for category in self.bot.guild.by_category():
            await ctx.send(self.format_message(category[0].name, category[1]))

    # commands with params
    @command(name=confs[3][0], help=confs[3][1], ignore_extra=False)
    async def list_membres_role(self, ctx, role_name):
        """ send a message with the list of members for a specific role
        or none message """
        role = self.check_param(self.bot.guild.roles, role_name)
        if isinstance(role, str):
            # no role with this name
            await ctx.send(role)
        else:
            role_members = []
            for member in self.bot.guild.members:
                self.add_condition(role_members, member, role in member.roles)
            await ctx.send(self.check_empty_list(role_name, role_members))

    @command(name=confs[4][0], help=confs[4][1], ignore_extra=False)
    async def list_membres_salon(self, ctx, channel_name):
        """ send a message with the list of members
        with permission on a channel"""
        # get channel
        channel = self.check_param(self.bot.guild.channels, channel_name)
        if isinstance(channel, str):
            # no channel with this name
            await ctx.send(channel)
        else:
            auth_members = []
            for member in self.bot.guild.members:
                self.add_condition(
                    auth_members, member,
                    channel.permissions_for(member).view_channel)
            await ctx.send(self.check_empty_list(channel_name, auth_members))
