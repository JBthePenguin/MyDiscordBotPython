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
        """ init with a user, a guild, a list of roles (id)
        and MagicMock for state """
        mem_data = {'user': user, 'roles': roles}
        super().__init__(data=mem_data, guild=guild, state=MagicMock())

    def name_id_update(self, user):
        " update id, name, bot, avatar, discriminator using user's properties"
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
        and MagicMock for state. *** @everyone have same id than guild *** """
        role_data = {'id': id, 'name': name, 'position': position}
        if permissions is True:
            print('yo')
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
        allow = permission[0].value
        deny = permission[1].value
        for r in roles:
            self.append(
                {"id": r.id, "type": 'role', 'allow': allow, 'deny': deny})
        for m in members:
            self.append(
                {"id": m.id, "type": 'member', 'allow': allow, 'deny': deny})


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

    def __init__(self, name, guild, type, position, roles=[], members=[]):
        """ init with a FakeChannelData (add 'type' = (text->0 news->5)),
        a guild, and MagicMock for state """
        channel_data = FakeChannelData(name, position, roles, members)
        channel_data['type'] = type
        super().__init__(data=channel_data, guild=guild, state=MagicMock())


class FakeVoiceChannel(VoiceChannel):
    """ Class to fake a voice channel """

    def __init__(self, name, guild, position, roles=[], members=[]):
        """ init with a FakeChannelData, a guild and MagicMock for state """
        channel_data = FakeChannelData(name, position, roles, members)
        super().__init__(data=channel_data, guild=guild, state=MagicMock())


class FakeGuild(Guild):
    """ Class to fake a guild """

    def __init__(self, name, members, roles, channels, owner_id):
        """ init with id, name,
        list of tuple for members (FakeUser, roles(list of name)),
        list of tuple for roles (name, position, permissions(bool)),
        list of tuple for channels (name, type, position, roles, members),
        a owner id and MagicMock for state """
        guild_data = {
            'id': next(discord_id), 'name': name, 'members': members,
            'channels': channels, 'roles': roles, 'owner_id': owner_id}
        super().__init__(data=guild_data, state=MagicMock())

    def _from_data(self, guild):
        """ override _from_data method (called at the end of Guild init)
        to customize init with properties
        -id -name -description -roles -members -owner -emojis -channels """
        self.id = int(guild['id'])
        self.name = guild.get('name')
        self.description = guild.get('description')
        self._roles = {}
        # add default role @everyone with the same id than the guild
        default_role = FakeRole(
            id=self.id, name='@everyone', guild=self, position=0,
            permissions=False)
        self._roles[default_role.id] = default_role
        # add roles
        name_id_roles = {}
        for name_pos in guild.get('roles', []):
            role = FakeRole(
                id=next(discord_id), name=name_pos[0], guild=self,
                position=name_pos[1], permissions=name_pos[2])
            self._roles[role.id] = role
            name_id_roles[role.name] = role.id
        # add members with roles
        for user_roles in guild.get('members', []):
            m_roles = []
            for role_name in user_roles[1]:
                m_roles.append(name_id_roles[role_name])
            member = FakeMember(user=user_roles[0], guild=self, roles=m_roles)
            member.name_id_update(user_roles[0])
            self._add_member(member)
        # add owner
        self.owner_id = guild.get('owner_id')
        self.emojis = guild.get('emojis', [])
        # add Channels:
        for name_type_pos in guild.get('channels', []):
            if name_type_pos[3] == 'all':
                roles = [self.default_role]
            else:
                roles = []
                for role_name in name_type_pos[3]:
                    role = self.get_role(name_id_roles[role_name])
                    roles.append(role)
            if name_type_pos[1] == 'TextChannel':
                channel = FakeTextChannel(
                    guild=self, name=name_type_pos[0],
                    type=0, position=name_type_pos[2], roles=roles)
                self._add_channel(channel)
            elif name_type_pos[1] == 'News':
                self._add_channel(FakeTextChannel(
                    guild=self, name=name_type_pos[0],
                    type=5, position=name_type_pos[2], roles=roles))
            elif name_type_pos[1] == 'VoiceChannel':
                self._add_channel(FakeVoiceChannel(
                    guild=self, name=name_type_pos[0],
                    position=name_type_pos[2], roles=roles))
            # elif c_type == ChannelType.category.value:
            #     self._add_channel(CategoryChannel(guild=self, data=c, state=self._state))
            # elif c_type == ChannelType.store.value:
            #     self._add_channel(StoreChannel(guild=self, data=c, state=self._state))


class FakeContext(MagicMock):
    """ Mock for a context with a fake guild """

    spec_set = Context(message=MagicMock(), prefix=MagicMock())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
