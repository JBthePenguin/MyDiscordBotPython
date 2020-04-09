from discord.ext.commands import Cog, command
from .settings import confs
from .format import info_in_shell, list_in_embed
from .checkers import param_command


class InfoCommands(Cog, name='Commands Info Team'):
    """ Class Category of commands to obtain infos on a team (guild) """

    def __init__(self, bot):
        self.bot = bot

    # commands without param
    @command(
            name=confs['shell']['name'],
            help=confs['shell']['help'], ignore_extra=False)
    async def shell_info(self, ctx):
        """ Display guild's infos in shell """
        info_in_shell(ctx.message.channel.guild)

    @command(
        name=confs['mem']['name'],
        help=confs['mem']['help'], ignore_extra=False)
    async def members(self, ctx):
        """ Send an embed with a sorted list of all members """
        guild = ctx.message.channel.guild
        await ctx.send(embed=list_in_embed(
            guild.members, guild.name, guild.icon_url, 'Members'))

    @command(
        name=confs['rol']['name'],
        help=confs['rol']['help'], ignore_extra=False)
    async def roles(self, ctx):
        """ Send an embed with the list of all roles """
        guild = ctx.message.channel.guild
        await ctx.send(embed=list_in_embed(
            guild.roles, guild.name, guild.icon_url, "Roles"))

    @command(
        name=confs['cat']['name'],
        help=confs['cat']['help'], ignore_extra=False)
    async def categories(self, ctx):
        """ Send an embed with the list of all channel's categories """
        guild = ctx.message.channel.guild
        await ctx.send(embed=list_in_embed(
            guild.categories, guild.name, guild.icon_url,
            "Channel's categories"))

    @command(
        name=confs['chan']['name'], help=confs['chan']['help'],
        ignore_extra=False)
    async def channels(self, ctx):
        """ Send an embed with the list of all channels (no send category) """
        guild = ctx.message.channel.guild
        channels = [  # remove categories in guild.channels
            chan for chan in guild.channels if chan not in guild.categories]
        await ctx.send(embed=list_in_embed(
            channels, guild.name, guild.icon_url, "Channels"))

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
        channels = [  # remove categories in guild.channels
            chan for chan in guild.channels if chan not in guild.categories]
        channel = param_command(channels, chan_name_or_id, 'Channel')
        ##### pb with vocal chan
        if isinstance(channel, str):  # no channel with this name or id
            await ctx.send(channel)
        else:
            await ctx.send(embed=list_in_embed(
                channel.members, channel.name, '', 'Auth Members'))
