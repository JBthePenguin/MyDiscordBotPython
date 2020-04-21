from discord import ChannelType
from discord.ext.commands import Cog, command
from .config import GUILD_COMMANDS as coms
from .shaping import GuildEmbed, GuildShell


class InfoGuildCommands(Cog, name='Commands Info Guild'):
    """ Class Category of commands to obtain infos for a guild """

    def __init__(self, bot):
        self.bot = bot

    @command(name=coms.gld.name, help=coms.gld.help, ignore_extra=False)
    async def guild(self, ctx):
        """ Send an embed with guild's stats """
        embed = GuildEmbed(ctx.guild.name, ctx.guild.icon_url)
        embed.add_title_stats(ctx.guild)
        await ctx.send(embed=embed)

    def make_objs_embed(self, name, icon_url, conf_embed, objs):
        """ Return an embed with a list of objects """
        embed = GuildEmbed(name, icon_url)
        embed.add_title_objs(conf_embed, objs)
        return embed

    @command(name=coms.own.name, help=coms.own.help, ignore_extra=False)
    async def owner(self, ctx):
        """ Send an embed with the owner """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url,
            coms.own.conf_embed, [ctx.guild.owner]))

    @command(name=coms.mem.name, help=coms.mem.help, ignore_extra=False)
    async def members(self, ctx):
        """ Send an embed with a list of all members """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url,
            coms.mem.conf_embed, ctx.guild.members))

    @command(name=coms.rol.name, help=coms.rol.help, ignore_extra=False)
    async def roles(self, ctx):
        """ Send an embed with a list of all roles """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url,
            coms.rol.conf_embed, ctx.guild.roles))

    @command(name=coms.cat.name, help=coms.cat.help, ignore_extra=False)
    async def categories(self, ctx):
        """ Send an embed with a list of all channel's categories """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url,
            coms.cat.conf_embed, ctx.guild.categories))

    @command(name=coms.cha.name, help=coms.cha.help, ignore_extra=False)
    async def channels(self, ctx):
        """ Send an embed with a list of all channels (no send category) """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url, coms.cha.conf_embed,
            [c for c in ctx.guild.channels if c.type != ChannelType.category]))

    @command(name=coms.tcha.name, help=coms.tcha.help, ignore_extra=False)
    async def text_channels(self, ctx):
        """ Send an embed with a list of all text channels """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url,
            coms.tcha.conf_embed,
            [c for c in ctx.guild.text_channels if not c.is_news()]))

    @command(name=coms.vcha.name, help=coms.vcha.help, ignore_extra=False)
    async def voice_channels(self, ctx):
        """ Send an embed with a list of all voice channels """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url,
            coms.vcha.conf_embed, ctx.guild.voice_channels))

    @command(name=coms.ncha.name, help=coms.ncha.help, ignore_extra=False)
    async def news_channels(self, ctx):
        """ Send an embed with a list of all news channels """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url, coms.ncha.conf_embed,
            [c for c in ctx.guild.channels if c.type == ChannelType.news]))

    @command(name=coms.scha.name, help=coms.scha.help, ignore_extra=False)
    async def store_channels(self, ctx):
        """ Send an embed with a list of all store channels """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url, coms.scha.conf_embed,
            [c for c in ctx.guild.channels if c.type == ChannelType.store]))

    @command(name=coms.emo.name, help=coms.emo.help, ignore_extra=False)
    async def emojis(self, ctx):
        """ Send an embed with a list of all emojis """
        await ctx.send(embed=self.make_objs_embed(
            ctx.guild.name, ctx.guild.icon_url,
            coms.emo.conf_embed, ctx.guild.emojis))

    @command(name=coms.shl.name, help=coms.shl.help, ignore_extra=False)
    async def shell_info(self, ctx):
        """ Display guild's infos in shell """
        guild_shell = GuildShell(ctx.guild)
        guild_shell.add_infos()
        print(guild_shell.infos)
        await ctx.send("Infos displayed in shell")
