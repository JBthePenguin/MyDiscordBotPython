from discord import Embed, ChannelType, Member, Role


class ComponentEmbed(Embed):
    """Embed for a Component."""

    def __init__(self, c_id, name, color, icon_url):
        """Init an embed with name for title, color,
        id for author name and icon_url."""
        super().__init__(title=name, color=color)
        self.set_author(name=f"id: {str(c_id)}", icon_url=icon_url)

    def add_list_in_field(self, objs, total_guild_objs, field_name):
        """Add a field after making a str with a list of objs"""
        # make the str value
        if len(objs) == total_guild_objs:
            objs_str = "All"
        elif not objs:
            objs_str = "None"
        else:
            objs.sort()
            objs_str = " - ".join(objs)
        # add field
        self.add_field(name=field_name, value=objs_str, inline=False)

    def add_auth_channels(self, obj):
        """Add field 'Channels allowed to view', for a role or a member,
        with value 'All' or 'None' or a string with auth channels's name."""
        channels = [
            c for c in obj.guild.channels if c.type != ChannelType.category]
        auth_channels = []
        # check permission view for each channel to make auth_channels
        if isinstance(obj, Member):
            # for member
            for channel in channels:
                if obj.permissions_in(channel).view_channel:
                    auth_channels.append(channel.name)
        elif isinstance(obj, Role):
            if obj.permissions.view_channel:
                # for role with view permission on all channels
                non_auth_chans = []
                for channel in channels:
                    # check permission overwrites for the channel
                    permission = channel.overwrites_for(obj)
                    if (permission.view_channel is not None) and (
                            not permission.view_channel):
                        # update the non auth channels list
                        non_auth_chans.append(channel)
                auth_channels = [
                    c.name for c in channels if c not in non_auth_chans]
            else:
                # for role without view permission on all channels
                for channel in channels:
                    if channel.overwrites_for(obj).view_channel:
                        auth_channels.append(channel.name)
        # add field
        self.add_list_in_field(
            auth_channels, len(channels), "Channels allowed to view")

    def add_member_infos(self, member, owner_id):
        """Add infos for a specific member:
        - description -> is bot or human, status.
        -fields -> roles and auth channels.
        -footer text -> member since; timestamp -> joined_at."""
        # desription -> bot or human and status, if owner.
        if member.bot:
            description = 'A bot '
        else:
            description = 'A human '
        description += f"actually {str(member.status)}."
        if member.id == owner_id:
            description += " He's the owner."
        self.description = description
        # roles
        self.add_list_in_field(
            [role.name for role in member.roles],
            len(member.guild.roles), "Roles")
        # auth channels (authorized to view)
        self.add_auth_channels(member)
        # footer and timestamp
        if member.joined_at is not None:
            self.set_footer(text="Member since")
            self.timestamp = member.joined_at

    def add_role_infos(self, role):
        """Add infos for a specific role:
        - description -> is bot or human, status.
        -fields -> members and auth channels.
        -footer text -> Created on; timestamp -> created_at."""
        # desription -> position.
        self.description = f"position: {str(role.position)}"
        # members
        self.add_list_in_field(
            [member.name for member in role.members],
            len(role.guild.members), "Members")
        # auth channels (authorized to view)
        self.add_auth_channels(role)
        # footer and timestamp
        self.set_footer(text="Created on")
        self.timestamp = role.created_at
