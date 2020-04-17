from unittest.mock import MagicMock
from discord import Guild, User, Member, Role, TextChannel, VoiceChannel
from discord.permissions import Permissions, PermissionOverwrite
from discord.ext.commands import Context
import itertools


discord_id = itertools.count(0)


class FakeUser(User):
    """ Class to fake a user """

    def __init__(self, username):
        """ init with an id, a username, a bot, a discriminator, an avatar
        and MagicMock for state """
        user_data = {
            'id': next(discord_id), 'username': username, 'bot': False,
            'discriminator': username, 'avatar': str(discord_id)}
        super().__init__(data=user_data, state=MagicMock())


class FakeMember(Member):
    """ Class to fake a member """

    def __init__(self, user, guild, roles):
        """ init with a user, a guild, a list of roles ids
        and MagicMock for state """
        mem_data = {'user': user, 'roles': roles}
        super().__init__(data=mem_data, guild=guild, state=MagicMock())

    def name_id_update(self, user):
        """ update id, name, bot, avatar, discriminator
        using the FakeUser's properties """
        u = self._user
        modified = (
            user.id, user.name, user.bot,
            user.avatar, user.discriminator)
        u.id, u.name, u.bot, u.avatar, u.discriminator = modified


class FakeRole(Role):
    """ Class to fake a role """

    def __init__(self, id, name, guild, position, permissions):
        """ init with an id, a name, a guild, a position,
        permissions (true -> add all permissions -> same as owner)
        and MagicMock for state.
        *** @everyone have same id than guild *** """
        role_data = {'id': id, 'name': name, 'position': position}
        if permissions is True:
            role_data['permissions'] = Permissions.all().value
        super().__init__(data=role_data, guild=guild, state=MagicMock())


class FakePermissionOverwrites(list):
    """ class to fake a permission overwrites list """

    def __init__(self, roles, members):
        """ init with read and send messages permissions for specific
        roles and members, *** used for argument in init FakeChannel ***
        -> [{'id': role or member id, 'type': 'role' or 'member',
        'allow': value, 'deny': value}, ...]  """
        super().__init__()
        permission = PermissionOverwrite(
            read_messages=True, send_messages=True).pair()
        allow, deny = permission[0].value, permission[1].value
        for role_id in roles:
            self.append(
                {"id": role_id, "type": 'role', 'allow': allow, 'deny': deny})
        for mem_id in members:
            self.append(
                {"id": mem_id, "type": 'member', 'allow': allow, 'deny': deny})


class FakeChannelData(dict):
    """ class to fake a channel data dict """

    def __init__(self, name, position, roles, members):
        """ init with keys id, name, position
        and permission_overwrites if there is role or member """
        super().__init__()
        self['id'] = next(discord_id)
        self['name'] = name
        self['position'] = position
        if roles or members:
            self['permission_overwrites'] = FakePermissionOverwrites(
                roles, members)


class FakeTextChannel(TextChannel):
    """ Class to fake a text channel """

    def __init__(self, name, guild, type, position, roles, members):
        """ init with a FakeChannelData (add 'type' = (text->0 news->5)),
        a guild, and MagicMock for state """
        channel_data = FakeChannelData(name, position, roles, members)
        channel_data['type'] = type
        super().__init__(data=channel_data, guild=guild, state=MagicMock())


class FakeVoiceChannel(VoiceChannel):
    """ Class to fake a voice channel """

    def __init__(self, name, guild, position, roles, members):
        """ init with a FakeChannelData, a guild and MagicMock for state """
        channel_data = FakeChannelData(name, position, roles, members)
        super().__init__(data=channel_data, guild=guild, state=MagicMock())


class FakeGuild(Guild):
    """ Class to fake a guild """

    def __init__(self, name, members, roles, channels, description=None):
        """ init with id, name, description(default=None)
        list of tuple for members (FakeUser, list of roles's name),
        list of tuple for roles (name, position, permissions(bool)),
        list of tuple for channels (name, type, position,
            roles and members names lists to overwrite permission
                or '@everyone' for roles to allow all members),
        *** first FakeUser in the members list will be the owner *** """
        guild_data = {
            'id': next(discord_id), 'name': name, 'members': members,
            'channels': channels, 'roles': roles}
        super().__init__(data=guild_data, state=MagicMock())

    def _from_data(self, guild):
        """ override _from_data method (called at the end of Guild init)
        to set properties with our custom datas ->
        -id -name -description -roles -members -owner -emojis -channels """
        # id - name - description
        self.id = int(guild['id'])
        self.name = guild.get('name')
        self.description = guild.get('description')
        # roles
        self._roles = {}
        # add default role @everyone with the same id than the guild
        default_role = FakeRole(
            id=self.id, name='@everyone', guild=self, position=0,
            permissions=False)
        self._roles[default_role.id] = default_role
        # add roles
        name_id_roles = {}  # used to add members and channels
        for tup_role in guild.get('roles'):
            role = FakeRole(
                id=next(discord_id), name=tup_role[0], guild=self,
                position=tup_role[1], permissions=tup_role[2])
            self._roles[role.id] = role
            name_id_roles[role.name] = role.id
        # add members (with their roles)
        for tup_member in guild.get('members'):
            m_roles = []  # list of member's roles ids
            for role_name in tup_member[1]:
                m_roles.append(name_id_roles[role_name])
            member = FakeMember(user=tup_member[0], guild=self, roles=m_roles)
            member.name_id_update(tup_member[0])
            self._add_member(member)
        # add owner (the first in members list)
        self.owner_id = self.members[0].id
        # add Channels:
        for tup_channel in guild.get('channels', []):
            # roles list to permission overwrite
            if tup_channel[3] == '@everyone':
                c_roles = [self.default_role.id]
            else:
                c_roles = []
                for role_name in tup_channel[3]:
                    c_roles.append(name_id_roles[role_name])
            # members list to permission overwrite
            c_members = []
            for member_name in tup_channel[4]:
                c_members.append(self.get_member_named(member_name).id)
            # Create Channel
            if tup_channel[1] == 'TextChannel':  # text
                channel = FakeTextChannel(
                    guild=self, name=tup_channel[0], type=0,
                    position=tup_channel[2], roles=c_roles, members=c_members)
            elif tup_channel[1] == 'News':  # news
                channel = FakeTextChannel(
                    guild=self, name=tup_channel[0], type=5,
                    position=tup_channel[2], roles=c_roles, members=c_members)
            elif tup_channel[1] == 'VoiceChannel':  # voice
                channel = FakeVoiceChannel(
                    guild=self, name=tup_channel[0], position=tup_channel[2],
                    roles=c_roles, members=c_members)
            self._add_channel(channel)
            # elif c_type == ChannelType.category.value:
            #     self._add_channel(CategoryChannel(guild=self, data=c, state=self._state))
            # elif c_type == ChannelType.store.value:
            #     self._add_channel(StoreChannel(guild=self, data=c, state=self._state))
        # add emojis
        self.emojis = guild.get('emojis', [])


class FakeContext(MagicMock):
    """ Mock for a context with a fake guild """

    spec_set = Context(message=MagicMock(), prefix=MagicMock())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
