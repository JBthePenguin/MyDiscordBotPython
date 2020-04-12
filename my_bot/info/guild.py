from discord import ChannelType
from discord.ext.commands import Cog, command
from .config import confs_guild as confs
from .config import (
    conf_shl, conf_own, conf_mem, conf_rol, conf_cat, conf_cha, conf_tcha,
    conf_vcha, conf_pcha, conf_gcha, conf_ncha, conf_scha, conf_emo)
from .shaping import info_in_shell, list_in_embed, emojis_in_embed
from .checking import GuildChecker


class InfoGuildCommands(Cog, name='Commands Info Guild'):
    """ Class Category of commands to obtain infos for a guild """

    def __init__(self, bot):
        self.bot = bot
        self.checker = GuildChecker()

    @command(name=conf_shl.name, help=conf_shl.help, ignore_extra=False)
    async def shell_info(self, ctx):
        """ Display guild's infos in shell """
        info_in_shell(ctx.message.channel.guild)

    async def respond(self, sender, name, icon_url, objs, confs_key):
        """ send a list in embed, if empty a message that indicate it"""
        objs_checked = self.checker.empty_content(
            objs, name, confs[confs_key]['obj_type'])
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

    @command(name=conf_own.name, help=conf_own.help, ignore_extra=False)
    async def owner(self, ctx):
        """ Send an embed with the owner """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [ctx.guild.owner], 'own')

    @command(name=conf_mem.name, help=conf_mem.help, ignore_extra=False)
    async def members(self, ctx):
        """ Send an embed with a sorted list of all members """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            ctx.guild.members, 'mem')

    @command(name=conf_rol.name, help=conf_rol.help, ignore_extra=False)
    async def roles(self, ctx):
        """ Send an embed with the list of all roles """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            ctx.guild.roles, 'rol')

    @command(name=conf_cat.name, help=conf_cat.help, ignore_extra=False)
    async def categories(self, ctx):
        """ Send an embed with the list of all channel's categories """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            ctx.guild.categories, 'cat')

    @command(name=conf_cha.name, help=conf_cha.help, ignore_extra=False)
    async def channels(self, ctx):
        """ Send an embed with the list of all channels (no send category) """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type != ChannelType.category],
            'cha')

    @command(name=conf_tcha.name, help=conf_tcha.help, ignore_extra=False)
    async def text_channels(self, ctx):
        """ Send an embed with the list of all text channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.text],
            'tcha')

    @command(name=conf_vcha.name, help=conf_vcha.help, ignore_extra=False)
    async def voice_channels(self, ctx):
        """ Send an embed with the list of all voice channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.voice],
            'vcha')

    @command(name=conf_pcha.name, help=conf_pcha.help, ignore_extra=False)
    async def private_channels(self, ctx):
        """ Send an embed with the list of all private channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.private],
            'pcha')

    @command(name=conf_gcha.name, help=conf_gcha.help, ignore_extra=False)
    async def group_channels(self, ctx):
        """ Send an embed with the list of all group channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.group],
            'gcha')

    @command(name=conf_ncha.name, help=conf_ncha.help, ignore_extra=False)
    async def news_channels(self, ctx):
        """ Send an embed with the list of all news channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.news],
            'ncha')

    @command(name=conf_scha.name, help=conf_scha.help, ignore_extra=False)
    async def store_channels(self, ctx):
        """ Send an embed with the list of all store channels """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            [c for c in ctx.guild.channels if c.type == ChannelType.store],
            'scha')

    @command(name=conf_emo.name, help=conf_emo.help, ignore_extra=False)
    async def emojis(self, ctx):
        """ Send an embed with the list of all emojis """
        await self.respond(
            ctx.send, ctx.guild.name, ctx.guild.icon_url,
            ctx.guild.emojis, 'emo')
