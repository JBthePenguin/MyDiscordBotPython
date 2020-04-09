from discord.ext.commands import Cog, command
from discord.utils import get as get_obj
from .settings import confs, error_msgs
from .format import info_in_shell, list_in_embed


class InfoCommands(Cog, name='Commands Info Team'):
    """ Class Category of commands to obtain infos on a team (guild) """

    def __init__(self, bot):
        self.bot = bot

    # commands without param
    @command(
            name=confs['shell']['name'], help=confs['shell']['help'],
            ignore_extra=False)
    async def shell_info(self, ctx):
        """ Display guild's infos in shell """
        info_in_shell(ctx.message.channel.guild)

    @command(
        name=confs['mem']['name'], help=confs['mem']['help'],
        ignore_extra=False)
    async def members(self, ctx):
        """ Send an embed with the list of all members """
        guild = ctx.message.channel.guild
        await ctx.send(embed=list_in_embed(
            guild.members, guild.name, guild.icon_url))

    @command(
        name=confs['rol']['name'], help=confs['rol']['help'],
        ignore_extra=False)
    async def roles(self, ctx):
        """ Send an embed with the list of all roles """
        guild = ctx.message.channel.guild
        await ctx.send(embed=list_in_embed(
            guild.roles, guild.name, guild.icon_url, "Roles"))

    @command(
        name=confs['chan']['name'], help=confs['chan']['help'],
        ignore_extra=False)
    async def channels(self, ctx):
        """ Send an embed with the list of all channels by category """
        guild = ctx.message.channel.guild
        for chans_by_cat in guild.by_category():
            if chans_by_cat[0] is None:
                cat_name = "No category"
            else:
                cat_name = "{} || {}".format(
                    str(chans_by_cat[0].id), chans_by_cat[0].name)
            await ctx.send(embed=list_in_embed(
                chans_by_cat[1], cat_name, '', 'Channels'))

    # commands with params
    def check_param(self, list_obj, obj_name_or_id):
        """ Check if obj is founded, return obj or a not exist message """
        obj = get_obj(list_obj, name=obj_name_or_id)
        if obj is None:
            try:
                obj = get_obj(list_obj, id=int(obj_name_or_id))
            except ValueError:  # no obj with this name
                return error_msgs['no_exist'].format('name', obj_name_or_id)
            else:
                if obj is None:  # no obj with this id
                    return error_msgs['no_exist'].format('id', obj_name_or_id)
        return obj

    @command(
            name=confs['rol_mem']['name'], help=confs['rol_mem']['help'],
            ignore_extra=False)
    async def role_members(self, ctx, role_name_or_id):
        """ Send an embed with the list of members with a specific role """
        guild = ctx.message.channel.guild
        role = self.check_param(guild.roles, role_name_or_id)
        if isinstance(role, str):  # no role with this name or id
            await ctx.send(role)
        else:
            await ctx.send(embed=list_in_embed(
                role.members, "{} || {}".format(str(role.id), role.name), ''))

    @command(
        name=confs['chan_mem']['name'], help=confs['chan_mem']['help'],
        ignore_extra=False)
    async def chan_members(self, ctx, chan_name_or_id):
        """ Send a message with the list of members
        who have view permission on a specific channel """
        guild = ctx.message.channel.guild
        channel = self.check_param(guild.channels, chan_name_or_id)
        if isinstance(channel, str):  # no channel with this name or id
            await ctx.send(channel)
        else:
            auth_members = []
            for member in guild.members:  # list member with permisson
                if channel.permissions_for(member).view_channel is True:
                    auth_members.append(member)
            await ctx.send(embed=list_in_embed(
                auth_members, "{} || {}".format(str(channel.id), channel.name),
                '', 'Auth Members'))
