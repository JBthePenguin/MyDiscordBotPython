from discord import ChannelType
from discord.ext.commands import Cog, command
from .config import (
    conf_shl, conf_own, conf_mem, conf_rol, conf_cat, conf_cha, conf_tcha,
    conf_vcha, conf_pcha, conf_gcha, conf_ncha, conf_scha, conf_emo)
from .shaping import GuildEmbed


class InfoGuildCommands(Cog, name='Commands Info Guild'):
    """ Class Category of commands to obtain infos for a guild """

    def __init__(self, bot):
        self.bot = bot

    # @command(name=conf_shl.name, help=conf_shl.help, ignore_extra=False)
    # async def shell_info(self, ctx):
    #     """ Display guild's infos in shell """
    #     info_in_shell(ctx.message.channel.guild)

    @command(name=conf_own.name, help=conf_own.help, ignore_extra=False)
    async def owner(self, ctx):
        """ Send an embed with the owner """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_own.conf_embed, [ctx.guild.owner]))

    @command(name=conf_mem.name, help=conf_mem.help, ignore_extra=False)
    async def members(self, ctx):
        """ Send an embed with a sorted list of all members """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_mem.conf_embed, ctx.guild.members))

    @command(name=conf_rol.name, help=conf_rol.help, ignore_extra=False)
    async def roles(self, ctx):
        """ Send an embed with the list of all roles """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_rol.conf_embed, ctx.guild.roles))

    @command(name=conf_cat.name, help=conf_cat.help, ignore_extra=False)
    async def categories(self, ctx):
        """ Send an embed with the list of all channel's categories """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_cat.conf_embed, ctx.guild.categories))

    @command(name=conf_cha.name, help=conf_cha.help, ignore_extra=False)
    async def channels(self, ctx):
        """ Send an embed with the list of all channels (no send category) """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_cha.conf_embed, [c for c in ctx.guild.channels if (
                    c.type != ChannelType.category)]))

    @command(name=conf_tcha.name, help=conf_tcha.help, ignore_extra=False)
    async def text_channels(self, ctx):
        """ Send an embed with the list of all text channels """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_tcha.conf_embed, ctx.guild.text_channels))

    @command(name=conf_vcha.name, help=conf_vcha.help, ignore_extra=False)
    async def voice_channels(self, ctx):
        """ Send an embed with the list of all voice channels """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_vcha.conf_embed, ctx.guild.voice_channels))

    @command(name=conf_pcha.name, help=conf_pcha.help, ignore_extra=False)
    async def private_channels(self, ctx):
        """ Send an embed with the list of all private channels """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_pcha.conf_embed, [c for c in ctx.guild.channels if (
                    c.type == ChannelType.private)]))

    @command(name=conf_gcha.name, help=conf_gcha.help, ignore_extra=False)
    async def group_channels(self, ctx):
        """ Send an embed with the list of all group channels """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_gcha.conf_embed, [c for c in ctx.guild.channels if (
                    c.type == ChannelType.group)]))

    @command(name=conf_ncha.name, help=conf_ncha.help, ignore_extra=False)
    async def news_channels(self, ctx):
        """ Send an embed with the list of all news channels """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_ncha.conf_embed, [c for c in ctx.guild.channels if (
                    c.type == ChannelType.news)]))

    @command(name=conf_scha.name, help=conf_scha.help, ignore_extra=False)
    async def store_channels(self, ctx):
        """ Send an embed with the list of all store channels """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_scha.conf_embed, [c for c in ctx.guild.channels if (
                    c.type == ChannelType.store)]))

    @command(name=conf_emo.name, help=conf_emo.help, ignore_extra=False)
    async def emojis(self, ctx):
        """ Send an embed with the list of all emojis """
        await ctx.send(embed=GuildEmbed(
            ctx.guild.name, ctx.guild.icon_url).add_title_objs(
                conf_emo.conf_embed, ctx.guild.emojis))
