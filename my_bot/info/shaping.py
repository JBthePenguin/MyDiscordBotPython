from discord import Embed, ChannelType
from .config import GUILD_TITLES as titles


class GuildEmbed(Embed):
    """Embed for a Guild."""

    def __init__(self, name, icon_url):
        """Init an embed with color, guild name and icon_url."""
        super().__init__(color=0x161616)
        self.set_author(name=name, icon_url=icon_url)

    def add_stat(self, title, objs):
        """Add a field, set name with default title,
        and value with the number of objs."""
        self.add_field(name=title.default, value=str(len(objs)), inline=True)

    def add_title_stats(self, guild):
        """Add title with owner name,
        add fields for guild's stats (number of members, roles,...)."""
        self.title = f"id: {guild.id}"
        self.add_stat(titles.mem, guild.members)
        self.add_stat(titles.rol, guild.roles)
        self.add_stat(titles.emo, guild.emojis)
        self.add_stat(titles.cat, guild.categories)
        self.add_stat(
            titles.cha,
            [c for c in guild.channels if c.type != ChannelType.category])
        self.add_stat(
            titles.tcha,
            [c for c in guild.text_channels if not c.is_news()])
        self.add_stat(titles.vcha, guild.voice_channels)
        self.add_stat(
            titles.ncha,
            [c for c in guild.channels if c.type == ChannelType.news])
        self.add_stat(
            titles.scha,
            [c for c in guild.channels if c.type == ChannelType.store])
        self.set_footer(text=f"{titles.own.default}: {guild.owner.name}")

    def add_title_objs(self, conf_embed, objs):
        """Add title, add fields id and name, add each obj sorted by name."""
        if objs:
            self.title = conf_embed.default
            if self.title == 'Emojis':  # for emoji
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                ids = "\n".join([str(obj.id) for obj in objs])
                names = "\n".join([obj.name for obj in objs])
                self.add_field(name='ID', value=ids, inline=True)
                self.add_field(name='Name', value=names, inline=True)
            self.set_footer(text=f"Total: {str(len(objs))}")
        else:  # no obj
            self.title = conf_embed.no_obj

    def add_emojis(self, emojis):
        """Add emojis(tuple) symbol and name, separate in 2 fields."""
        half_n_emo = len(emojis) // 2
        first_emos = [emo for emo in emojis[half_n_emo:]]
        second_emos = [emo for emo in emojis[:half_n_emo]]
        first_field = "\n\n".join([
            f'{str(emoji)} {emoji.name}' for emoji in first_emos])
        second_field = "\n\n".join([
            f'{str(emoji)} {emoji.name}' for emoji in second_emos])
        self.add_field(name='\u200b', value=first_field, inline=True)
        self.add_field(name='\u200b', value=second_field, inline=True)


class GuildShell():
    """String for a Guild."""

    def __init__(self, guild):
        """Init a string for infos with guild id and name."""
        self.guild = guild
        self.infos = ''

    def add_list(self, title, objs):
        """Add a list with a title to infos string."""
        if objs:
            if (title.default == 'Guild') or (title.default == 'Owner'):
                n_objs = ''
            else:
                n_objs = str(len(objs))
            self.infos += f"\n########## {n_objs} {title.default} ##########\n"
            if title.default == 'Emojis':
                self.add_emojis(objs)
            else:
                objs.sort(key=lambda obj: obj.name)
                for obj in objs:
                    self.infos += f"- {obj.id} - {obj.name}\n"
        else:
            self.infos += f"\n########## {title.no_obj} ##########\n"

    def add_emojis(self, emojis):
        """Add a tuple of emojis (3 by line)."""
        i = 0
        for emoji in emojis:
            self.infos += f"- {str(emoji)} {emoji.name} "
            if i == 2:
                self.infos += "\n"
                i = 0
            else:
                i += 1

    def add_type_chans(self, chans, title):
        """Add channels with a specific type(title)."""
        if chans:
            self.infos += f"### {str(len(chans))} {title.default}\n"
            chans.sort(key=lambda chan: chan.name)
            for chan in chans:
                self.infos += f"- {chan.id} - {chan.name}\n"

    def add_cats_chans(self, chans_cats):
        """Add channels by category and type."""
        if chans_cats:
            self.infos += "\n\n########## CHANNELS BY CATEGORIES ##########\n"
            for chans_cat in chans_cats:
                if chans_cat[0] is None:
                    self.infos += f"\n##### {titles.cat.no_obj} #####\n"
                else:
                    self.infos += f"\n##### {chans_cat[0].name} #####\n"
                if chans_cat[1]:
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.text)], titles.tcha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.voice)], titles.vcha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.news)], titles.ncha)
                    self.add_type_chans(
                        [c for c in chans_cat[1] if (
                            c.type == ChannelType.store)], titles.scha)
                else:
                    self.infos += f"- {titles.cha.no_obj}\n"

    def add_infos(self):
        """Construct a string with all guild's infos."""
        # guild and owner
        self.add_list(titles.gld, [self.guild])
        self.add_list(titles.own, [self.guild.owner])
        # members, roles, channel's categories, channels
        self.add_list(titles.mem, self.guild.members)
        self.add_list(titles.rol, self.guild.roles)
        self.add_list(titles.cat, self.guild.categories)
        self.add_list(
            titles.cha,
            [c for c in self.guild.channels if c.type != ChannelType.category])
        # text, voice, private, group, news and store channels
        self.add_list(
            titles.tcha,
            [c for c in self.guild.text_channels if not c.is_news()])
        self.add_list(titles.vcha, self.guild.voice_channels)
        self.add_list(
            titles.ncha,
            [c for c in self.guild.channels if c.type == ChannelType.news])
        self.add_list(
            titles.scha,
            [c for c in self.guild.channels if c.type == ChannelType.store])
        # Emojis
        self.add_list(titles.emo, self.guild.emojis)
        # Channels by Category
        self.add_cats_chans(self.guild.by_category())


class ComponentEmbed(Embed):
    """Embed for a Component."""

    def __init__(self, c_id, name, color, icon_url):
        """Init an embed with name for title, color,
        id for author name and icon_url."""
        super().__init__(title=name, color=color)
        self.set_author(name=f"id: {str(c_id)}", icon_url=icon_url)

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
        roles = " - ".join([role.name for role in member.roles])
        self.add_field(name="Roles", value=roles, inline=False)
        # auth channels (authorized to view)
        channels = [c for c in member.guild.channels if (
            c.type != ChannelType.category)]
        auth_channels = []
        for channel in channels:
            if member.permissions_in(channel).view_channel:
                auth_channels.append(channel.name)
        if len(auth_channels) == len(channels):
            auth_channels_str = "All"
        elif auth_channels:
            auth_channels.sort()
            auth_channels_str = " - ".join(auth_channels)
        else:
            auth_channels_str = "None"
        self.add_field(
            name="Channels allowed to view", value=auth_channels_str,
            inline=False)
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
        members = [member.name for member in role.members]
        if len(members) == len(role.guild.members):
            members_str = "All"
        else:
            members_str = " - ".join(members)
        self.add_field(name="Members", value=members_str, inline=False)
        # auth channels (authorized to view)
        channels = [c for c in role.guild.channels if (
            c.type != ChannelType.category)]
        if role.permissions.view_channel:
            # for role with view permission on all channels
            non_auth_chans = []
            for channel in channels:
                # check permission overwrites for the channel
                permission = channel.overwrites_for(role)
                if (permission.view_channel is not None) and (
                        not permission.view_channel):
                    # update the non auth channels list
                    non_auth_chans.append(channel)
            if non_auth_chans:
                auth_channels = [
                    c.name for c in channels if c not in non_auth_chans]
                auth_channels.sort()
                auth_channels_str = " - ".join(auth_channels)
            else:
                auth_channels_str = "All"
        else:
            # for role without view permission on all channels
            auth_channels = []
            for channel in channels:
                # check permission overwrites for the channel
                if channel.overwrites_for(role).view_channel:
                    # update the non auth channels list
                    auth_channels.append(channel.name)
            if len(auth_channels) == len(channels):
                auth_channels_str = "All"
            elif auth_channels:
                auth_channels.sort()
                auth_channels_str = " - ".join(auth_channels)
            else:
                auth_channels_str = "None"
        self.add_field(
            name="Channels allowed to view", value=auth_channels_str,
            inline=False)
        # footer and timestamp
        self.set_footer(text="Created on")
        self.timestamp = role.created_at
