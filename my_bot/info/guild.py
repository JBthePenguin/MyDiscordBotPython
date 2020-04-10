from discord import ChannelType
from discord.ext.commands import Cog, command
from .settings import confs
from .format import info_in_shell, list_in_embed
from .checkers import list_content


class InfoGuildCommands(Cog, name='Commands Info Guild'):
    """ Class Category of commands to obtain infos for a guild """

    def __init__(self, bot):
        self.bot = bot

    @command(
            name=confs['shl']['name'],
            help=confs['shl']['help'], ignore_extra=False)
    async def shell_info(self, ctx):
        """ Display guild's infos in shell """
        info_in_shell(ctx.message.channel.guild)

    async def respond(self, guild, sender, objs, obj_type, objs_type):
        """ send a list in embed, if is empty one a message that indicate it"""
        objs_checked = list_content(objs, guild.name, obj_type)
        if isinstance(objs_checked, str):
            await sender(objs_checked)
        else:
            await sender(embed=list_in_embed(
                objs_checked, guild.name, guild.icon_url, objs_type))

    @command(
        name=confs['mem']['name'],
        help=confs['mem']['help'], ignore_extra=False)
    async def members(self, ctx):
        """ Send an embed with a sorted list of all members """
        guild = ctx.message.channel.guild
        await self.respond(guild, ctx.send, guild.members, 'member', 'Members')
        # members = list_content(guild.members, guild.name, 'member')
        # if isinstance(members, str):
        #     await ctx.send(members)
        # else:
        #     await ctx.send(embed=list_in_embed(
        #         members, guild.name, guild.icon_url, 'Members'))

    @command(
        name=confs['rol']['name'],
        help=confs['rol']['help'], ignore_extra=False)
    async def roles(self, ctx):
        """ Send an embed with the list of all roles """
        guild = ctx.message.channel.guild
        roles = list_content(guild.roles, guild.name, 'role')
        if isinstance(roles, str):
            await ctx.send(roles)
        else:
            await ctx.send(embed=list_in_embed(
                roles, guild.name, guild.icon_url, "Roles"))

    @command(
        name=confs['cat']['name'],
        help=confs['cat']['help'], ignore_extra=False)
    async def categories(self, ctx):
        """ Send an embed with the list of all channel's categories """
        guild = ctx.message.channel.guild
        cats = list_content(guild.categories, guild.name, 'channel category')
        if isinstance(cats, str):
            await ctx.send(cats)
        else:
            await ctx.send(embed=list_in_embed(
                cats, guild.name, guild.icon_url, "Channel's categories"))

    @command(
        name=confs['cha']['name'],
        help=confs['cha']['help'], ignore_extra=False)
    async def channels(self, ctx):
        """ Send an embed with the list of all channels (no send category) """
        guild = ctx.message.channel.guild
        channels = list_content(
            [c for c in guild.channels if c.type != ChannelType.category],
            guild.name, 'channel')
        if isinstance(channels, str):
            await ctx.send(channels)
        else:
            await ctx.send(embed=list_in_embed(
                channels, guild.name, guild.icon_url, "Channels"))

    @command(
        name=confs['tcha']['name'],
        help=confs['tcha']['help'], ignore_extra=False)
    async def text_channels(self, ctx):
        """ Send an embed with the list of all text channels """
        guild = ctx.message.channel.guild
        t_channels = list_content(
            [c for c in guild.channels if c.type == ChannelType.text],
            guild.name, 'text channel')
        if isinstance(t_channels, str):
            await ctx.send(t_channels)
        else:
            await ctx.send(embed=list_in_embed(
                t_channels, guild.name, guild.icon_url, "Text Channels"))

    @command(
        name=confs['vcha']['name'],
        help=confs['vcha']['help'], ignore_extra=False)
    async def voice_channels(self, ctx):
        """ Send an embed with the list of all voice channels """
        guild = ctx.message.channel.guild
        v_channels = list_content(
            [c for c in guild.channels if c.type == ChannelType.voice],
            guild.name, 'voice channel')
        if isinstance(v_channels, str):
            await ctx.send(v_channels)
        else:
            await ctx.send(embed=list_in_embed(
                v_channels, guild.name, guild.icon_url, "Voice Channels"))
