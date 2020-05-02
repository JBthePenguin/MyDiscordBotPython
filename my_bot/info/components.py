from discord.ext.commands import Cog, command
from .config import COMPONENTS_COMMANDS as coms
from .shaping import ComponentEmbed


def check_parameter(param, get_by_id, get_by_name):
    """Check if an obj with id or name exist, return it,
    or a not founded message."""
    try:
        obj_id = int(param)
    except ValueError:
        # name
        obj = get_by_name(param)
        if obj is None:
            return f"with name {param} not founded."
    else:
        # id
        obj = get_by_id(obj_id)
        if obj is None:
            return f"with id {param} not founded."
    return obj


class InfoComponentsCommands(Cog, name='Commands Info Components'):
    """Class Category of commands to obtain infos for guild's components."""

    def __init__(self, bot):
        self.bot = bot

    @command(name=coms.mem.name, help=coms.mem.help, ignore_extra=False)
    async def member(self, ctx, id_or_name):
        """Send an embed with info for a specific member."""
        member = check_parameter(
            id_or_name, ctx.guild.get_member, ctx.guild.get_member_named)
        if isinstance(member, str):
            # no member founded
            await ctx.send(f"Member {member}")
        else:
            embed = ComponentEmbed(
                member.id, member.name, member.color, member.avatar_url)
            embed.add_member_infos(member, ctx.guild.owner_id)
            await ctx.send(embed=embed)
