from discord.ext.commands import Cog, command
from discord.utils import get as get_obj
from discord import Embed

# Configurations of commands -> [[name, help], [name, help], ...]
confs = [
    ['shell_info', 'Display infos in shell -> #shell_info'],
    ['members', "All guild's members-> #members"],
    ['roles', 'All roles-> #roles'],
    ['channels', 'All channels by category-> #channels'],
    ['role_members', 'Members for a role-> #role_members "role name or id"'],
    ['chan_members', 'Authorized Members -> #chan_members "chan name or id"']]


class InfoCommands(Cog, name='Commandes Info'):

    def __init__(self, bot):
        self.bot = bot

    # commands without param
    @command(name=confs[0][0], help=confs[0][1], ignore_extra=False)
    async def shell_info_guild(self, ctx):
        """ display infos in shell """
        # guild
        guild = ctx.message.channel.guild
        print('###########')
        print("Guild id: {} - {}".format(guild.id, guild.name))
        print('###########')
        # members
        for member in guild.members:
            print("Member id: {} - {}".format(member.id, member.name))
        print('#####')
        # roles
        for role in guild.roles:
            print("Role id: {} - {}".format(role.id, role.name))
        # channel categories
        for chans_by_cat in guild.by_category():
            print('#####')
            if chans_by_cat[0] is None:
                print("Cat None")
            else:
                print(
                    "Category id: {} - {}".format(
                        chans_by_cat[0].id, chans_by_cat[0].name))
            # channels
            for channel in chans_by_cat[1]:
                print(
                    "-- Chan -- id: {} - {}".format(channel.id, channel.name))

    def format_list_in_embed(self, objs, author_name, icon_url, title="Members"):
        """ return an embed with a list """
        objs_ids = "\n".join(str(obj.id) for obj in objs)
        objs_names = "\n".join(obj.name for obj in objs)
        embed = Embed(title=title, color=0x161616)
        embed.set_author(name=author_name, icon_url=icon_url)
        embed.add_field(name='ID', value=objs_ids, inline=True)
        embed.add_field(name='Name', value=objs_names, inline=True)
        return embed

    @command(name=confs[1][0], help=confs[1][1], ignore_extra=False)
    async def members(self, ctx):
        """ send an embed with the list of all members """
        guild = ctx.message.channel.guild
        await ctx.send(embed=self.format_list_in_embed(
            guild.members, guild.name, guild.icon_url))

    @command(name=confs[2][0], help=confs[2][1], ignore_extra=False)
    async def roles(self, ctx):
        """ send an embed with the list of all roles """
        guild = ctx.message.channel.guild
        await ctx.send(embed=self.format_list_in_embed(
            guild.roles, guild.name, guild.icon_url, "Roles"))

    @command(name=confs[3][0], help=confs[3][1], ignore_extra=False)
    async def channels(self, ctx):
        """ send an embed with the list of all channels by category """
        guild = ctx.message.channel.guild
        for chans_by_cat in guild.by_category():
            await ctx.send(embed=self.format_list_in_embed(
                chans_by_cat[1],
                "{} || {}".format(
                    str(chans_by_cat[0].id), chans_by_cat[0].name),
                '', 'Channels'))

    # commands with params
    def check_param(self, list_obj, obj_name_or_id):
        """ Check if parameter is Ok, return the corresponding object if it is
        or a not exist message if not """
        obj = get_obj(list_obj, name=obj_name_or_id)
        if obj is None:
            try:
                obj = get_obj(list_obj, id=int(obj_name_or_id))
            except ValueError:
                # no role with this name
                return "name: {} not exist".format(obj_name_or_id)
            else:
                if obj is None:
                    # no role with this id
                    return "id: {} not exist".format(obj_name_or_id)
        return obj

    @command(name=confs[4][0], help=confs[4][1], ignore_extra=False)
    async def role_members(self, ctx, role_name_or_id):
        """ send an embed with the list of members for a specific role """
        guild = ctx.message.channel.guild
        role = self.check_param(guild.roles, role_name_or_id)
        if isinstance(role, str):
            # no role with this name or id
            await ctx.send(role)
        else:
            await ctx.send(embed=self.format_list_in_embed(
                role.members, "{} || {}".format(str(role.id), role.name), ''))

    @command(name=confs[5][0], help=confs[5][1], ignore_extra=False)
    async def chan_members(self, ctx, chan_name_or_id):
        """ send a message with the list of members
        with permission on a channel"""
        # get channel
        guild = ctx.message.channel.guild
        channel = self.check_param(guild.channels, chan_name_or_id)
        if isinstance(channel, str):
            # no channel with this name or id
            await ctx.send(channel)
        else:
            auth_members = []
            for member in guild.members:
                if channel.permissions_for(member).view_channel is True:
                    auth_members.append(member)
            await ctx.send(embed=self.format_list_in_embed(
                auth_members, "{} || {}".format(str(channel.id), channel.name),
                ''))
