from discord.ext.commands import Cog, command
from .config import GUILD_COMMANDS as coms
from .shapers import GuildEmbed, GuildShell


class InfoGuildCommands(Cog, name='Commands Info Guild'):
    """Class Category of commands to obtain infos for a guild."""

    def __init__(self, bot):
        self.bot = bot

    @command(name=coms['gld'][0], help=coms['gld'][1], ignore_extra=False)
    async def guild(self, ctx):
        """Send an embed with guild's stats."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'gld'))

    @command(name=coms['own'][0], help=coms['own'][1], ignore_extra=False)
    async def owner(self, ctx):
        """Send an embed with the owner."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'own'))

    @command(name=coms['mem'][0], help=coms['mem'][1], ignore_extra=False)
    async def members(self, ctx):
        """Send an embed with a list of all members."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'mem'))

    @command(name=coms['rol'][0], help=coms['rol'][1], ignore_extra=False)
    async def roles(self, ctx):
        """Send an embed with a list of all roles."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'rol'))

    @command(name=coms['cat'][0], help=coms['cat'][1], ignore_extra=False)
    async def categories(self, ctx):
        """Send an embed with a list of all channel's categories."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'cat'))

    @command(name=coms['cha'][0], help=coms['cha'][1], ignore_extra=False)
    async def channels(self, ctx):
        """Send an embed with a list of all channels (no send category)."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'cha'))

    @command(name=coms['tcha'][0], help=coms['tcha'][1], ignore_extra=False)
    async def text_channels(self, ctx):
        """Send an embed with a list of all text channels."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'tcha'))

    @command(name=coms['vcha'][0], help=coms['vcha'][1], ignore_extra=False)
    async def voice_channels(self, ctx):
        """Send an embed with a list of all voice channels."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'vcha'))

    @command(name=coms['ncha'][0], help=coms['ncha'][1], ignore_extra=False)
    async def news_channels(self, ctx):
        """Send an embed with a list of all news channels."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'ncha'))

    @command(name=coms['scha'][0], help=coms['scha'][1], ignore_extra=False)
    async def store_channels(self, ctx):
        """Send an embed with a list of all store channels."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'scha'))

    @command(name=coms['emo'][0], help=coms['emo'][1], ignore_extra=False)
    async def emojis(self, ctx):
        """Send an embed with a list of all emojis."""
        await ctx.send(embed=GuildEmbed(ctx.guild, 'emo'))

    @command(name=coms['shl'][0], help=coms['shl'][1], ignore_extra=False)
    async def shell_info(self, ctx):
        """Display guild's infos in shell."""
        # GuildShell(ctx.guild)
        print(GuildShell(ctx.guild))
        # print('raaaaa')
        # guild_shell = GuildShell(ctx.guild)
        # guild_shell.add_infos()
        # print(guild_shell.infos)
        await ctx.send("Infos displayed in shell")
