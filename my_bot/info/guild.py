from discord import ChannelType
from discord.ext.commands import Cog, command
from .config import (
    com_own, com_mem, com_rol, com_cat, com_cha, com_tcha, com_vcha, com_pcha,
    com_gcha, com_ncha, com_scha, com_emo, com_shl)
from .shaping import GuildEmbed, GuildShell


class InfoGuildCommands(Cog, name='Commands Info Guild'):
    """ Class Category of commands to obtain infos for a guild """

    def __init__(self, bot):
        self.bot = bot

    def make_embed(self, name, icon_url, conf_embed, objs):
        """ Return an embed with a list of objects """
        embed = GuildEmbed(name, icon_url)
        embed.add_title_objs(conf_embed, objs)
        return embed

    @command(name=com_own.name, help=com_own.help, ignore_extra=False)
    async def owner(self, ctx):
        """ Send an embed with the owner """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url,
            com_own.conf_embed, [ctx.guild.owner]))
        # await self.respond(ctx, conf_own.conf_embed, [ctx.guild.owner])

    @command(name=com_mem.name, help=com_mem.help, ignore_extra=False)
    async def members(self, ctx):
        """ Send an embed with a list of all members """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url,
            com_mem.conf_embed, ctx.guild.members))

    @command(name=com_rol.name, help=com_rol.help, ignore_extra=False)
    async def roles(self, ctx):
        """ Send an embed with a list of all roles """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url,
            com_rol.conf_embed, ctx.guild.roles))

    @command(name=com_cat.name, help=com_cat.help, ignore_extra=False)
    async def categories(self, ctx):
        """ Send an embed with a list of all channel's categories """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url,
            com_cat.conf_embed, ctx.guild.categories))

    @command(name=com_cha.name, help=com_cha.help, ignore_extra=False)
    async def channels(self, ctx):
        """ Send an embed with a list of all channels (no send category) """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url, com_cha.conf_embed,
            [c for c in ctx.guild.channels if c.type != ChannelType.category]))

    @command(name=com_tcha.name, help=com_tcha.help, ignore_extra=False)
    async def text_channels(self, ctx):
        """ Send an embed with a list of all text channels """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url,
            com_tcha.conf_embed, ctx.guild.text_channels))

    @command(name=com_vcha.name, help=com_vcha.help, ignore_extra=False)
    async def voice_channels(self, ctx):
        """ Send an embed with a list of all voice channels """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url,
            com_vcha.conf_embed, ctx.guild.voice_channels))

    @command(name=com_pcha.name, help=com_pcha.help, ignore_extra=False)
    async def private_channels(self, ctx):
        """ Send an embed with a list of all private channels """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url, com_pcha.conf_embed,
            [c for c in ctx.guild.channels if c.type == ChannelType.private]))

    @command(name=com_gcha.name, help=com_gcha.help, ignore_extra=False)
    async def group_channels(self, ctx):
        """ Send an embed with a list of all group channels """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url, com_gcha.conf_embed,
            [c for c in ctx.guild.channels if c.type == ChannelType.group]))

    @command(name=com_ncha.name, help=com_ncha.help, ignore_extra=False)
    async def news_channels(self, ctx):
        """ Send an embed with a list of all news channels """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url, com_ncha.conf_embed,
            [c for c in ctx.guild.channels if c.type == ChannelType.news]))

    @command(name=com_scha.name, help=com_scha.help, ignore_extra=False)
    async def store_channels(self, ctx):
        """ Send an embed with a list of all store channels """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url, com_scha.conf_embed,
            [c for c in ctx.guild.channels if c.type == ChannelType.store]))

    @command(name=com_emo.name, help=com_emo.help, ignore_extra=False)
    async def emojis(self, ctx):
        """ Send an embed with a list of all emojis """
        await ctx.send(embed=self.make_embed(
            ctx.guild.name, ctx.guild.icon_url,
            com_emo.conf_embed, ctx.guild.emojis))

    @command(name=com_shl.name, help=com_shl.help, ignore_extra=False)
    async def shell_info(self, ctx):
        """ Display guild's infos in shell """
        guild_shell = GuildShell(ctx.guild)
        guild_shell.add_infos()
        print(guild_shell.infos)
