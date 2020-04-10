from discord import ChannelType
from discord.ext.commands import Cog, command
from .settings import confs_guild as confs
from .format import info_in_shell, list_in_embed, emojis_in_embed
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

    async def respond(self, sender, name, icon_url, objs, confs_key):
        """ send a list in embed, if empty a message that indicate it"""
        objs_checked = list_content(objs, name, confs[confs_key]['obj_type'])
        if isinstance(objs_checked, str):
            await sender(objs_checked)
        else:
            if confs_key == 'emo':
                embed = emojis_in_embed(
                    objs_checked, name, icon_url, confs[confs_key]['title'])
            else:
                embed = list_in_embed(
                    objs_checked, name, icon_url, confs[confs_key]['title'])
            await sender(embed=embed)

    @command(
        name=confs['own']['name'],
        help=confs['own']['help'], ignore_extra=False)
    async def owner(self, ctx):
        """ Send an embed with the owner """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [ctx.guild.owner], 'own')

    @command(
        name=confs['mem']['name'],
        help=confs['mem']['help'], ignore_extra=False)
    async def members(self, ctx):
        """ Send an embed with a sorted list of all members """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            ctx.guild.members, 'mem')

    @command(
        name=confs['rol']['name'],
        help=confs['rol']['help'], ignore_extra=False)
    async def roles(self, ctx):
        """ Send an embed with the list of all roles """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            ctx.guild.roles, 'rol')

    @command(
        name=confs['cat']['name'],
        help=confs['cat']['help'], ignore_extra=False)
    async def categories(self, ctx):
        """ Send an embed with the list of all channel's categories """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            ctx.guild.categories, 'cat')

    @command(
        name=confs['cha']['name'],
        help=confs['cha']['help'], ignore_extra=False)
    async def channels(self, ctx):
        """ Send an embed with the list of all channels (no send category) """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type != ChannelType.category],
            'cha')

    @command(
        name=confs['tcha']['name'],
        help=confs['tcha']['help'], ignore_extra=False)
    async def text_channels(self, ctx):
        """ Send an embed with the list of all text channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.text],
            'tcha')

    @command(
        name=confs['vcha']['name'],
        help=confs['vcha']['help'], ignore_extra=False)
    async def voice_channels(self, ctx):
        """ Send an embed with the list of all voice channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.voice],
            'vcha')

    @command(
        name=confs['pcha']['name'],
        help=confs['pcha']['help'], ignore_extra=False)
    async def private_channels(self, ctx):
        """ Send an embed with the list of all private channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.private],
            'pcha')

    @command(
        name=confs['gcha']['name'],
        help=confs['gcha']['help'], ignore_extra=False)
    async def group_channels(self, ctx):
        """ Send an embed with the list of all group channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.group],
            'gcha')

    @command(
        name=confs['ncha']['name'],
        help=confs['ncha']['help'], ignore_extra=False)
    async def news_channels(self, ctx):
        """ Send an embed with the list of all news channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.news],
            'ncha')

    @command(
        name=confs['scha']['name'],
        help=confs['scha']['help'], ignore_extra=False)
    async def store_channels(self, ctx):
        """ Send an embed with the list of all store channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.store],
            'scha')

    @command(
        name=confs['emo']['name'],
        help=confs['emo']['help'], ignore_extra=False)
    async def emojis(self, ctx):
        """ Send an embed with the list of all emojis """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            ctx.guild.emojis, 'emo')
