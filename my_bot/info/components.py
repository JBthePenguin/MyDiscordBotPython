from discord.ext.commands import Cog, command
from .config import COMPONENTS_COMMANDS as coms
from .shaping import ComponentEmbed


class InfoComponentsCommands(Cog, name='Commands Info Components'):
    """ Class Category of commands to obtain infos for guild's components """

    def __init__(self, bot):
        self.bot = bot

    def check_parameter(self, param, get_by_id, get_by_name):
        """ check if an obj with id or name exist
        return obj or a not founded message """
        try:
            id = int(param)
        except ValueError:
            # name
            obj = get_by_name(param)
            if obj is None:
                return f"with name {param} not founded."
        else:
            # id
            obj = get_by_id(id)
            if obj is None:
                return f"with id {param} not founded."
        return obj

    @command(name=coms.mem.name, help=coms.mem.help, ignore_extra=False)
    async def member(self, ctx, id_or_name):
        """ Send an embed with info for a specific member """
        member = self.check_parameter(
            id_or_name, ctx.guild.get_member, ctx.guild.get_member_named)
        if isinstance(member, str):
            # no member founded
            ctx.send(f"Member {member}")
        else:
            embed = ComponentEmbed(
                member.id, member.nick, member.description,
                member.color, member.avatar_url)
            ctx.send(embed=embed)
