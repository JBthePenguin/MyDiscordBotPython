from discord import ChannelType
from discord.ext.commands import Cog, command
from .settings import confs
from .format import info_in_shell, list_in_embed
from .checkers import param_command, list_content


class InfoCommands(Cog, name='Commands Info Team'):
    """ Class Category of commands to obtain infos for a team (guild) """

    def __init__(self, bot):
        self.bot = bot

    # # commands with params
    @command(
            name=confs['rol_mem']['name'], help=confs['rol_mem']['help'],
            ignore_extra=False)
    async def role_mems(self, ctx, role_name_or_id):
        """ Send an embed with the list of members for a specific role """
        guild = ctx.message.channel.guild
        role = param_command(guild.roles, role_name_or_id, 'Role')
        if isinstance(role, str):  # no role with this name or id
            await ctx.send(role)
        else:
            await ctx.send(embed=list_in_embed(
                role.members, role.name, '', 'Members'))

    @command(
            name=confs['cat_chan']['name'], help=confs['cat_chan']['help'],
            ignore_extra=False)
    async def cat_chans(self, ctx, cat_name_or_id):
        """ Send an embed with the list of channels for a specific category """
        guild = ctx.message.channel.guild
        category = param_command(
            guild.categories, cat_name_or_id, 'Channel Category')
        if isinstance(category, str):  # no category with this name or id
            await ctx.send(category)
        else:
            await ctx.send(embed=list_in_embed(
                category.channels, category.name, '', 'Channels'))

    @command(
        name=confs['chan_mem']['name'], help=confs['chan_mem']['help'],
        ignore_extra=False)
    async def chan_mems(self, ctx, chan_name_or_id):
        """ Send a message with the list of members
        who have view permission for a specific channel """
        guild = ctx.message.channel.guild
        channels = [  # remove category to the channels list
            c for c in guild.channels if c.type != ChannelType.category]
        channel = param_command(channels, chan_name_or_id, 'Channel')
        if isinstance(channel, str):  # no channel with this name or id
            await ctx.send(channel)
        else:
            await ctx.send(embed=list_in_embed(
                channel.members, channel.name, '', 'Auth Members'))
