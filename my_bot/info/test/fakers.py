from unittest.mock import MagicMock
from discord import Guild, User, Member, Role, TextChannel
from discord.enums import ChannelType
from discord.ext.commands import Context
import itertools


discord_id = itertools.count(0)


class FakeUser(User):
    """ Class to fake a user """

    def __init__(self, name):
        """ init a user with id, name, discriminator, avatar
        and MagicMock for state """
        user_data = {
            'id': next(discord_id), 'username': name,
            'discriminator': name, 'avatar': str(discord_id)}
        super().__init__(data=user_data, state=MagicMock())


class FakeMember(Member):
    """ Class to fake a member """

    def __init__(self, user, guild, roles):
        """ init a member with a user, a list of roles (id), a guild
        and MagicMock for state """
        mem_data = {'user': user, 'roles': roles}
        super().__init__(data=mem_data, guild=guild, state=MagicMock())

    def name_id_update(self, user):
        " update id, name, avatar, discriminator using user's properties"
        u = self._user
        modified = (user.id, user.name, user.avatar, user.discriminator)
        u.id, u.name, u.avatar, u.discriminator = modified


class FakeRole(Role):
    """ Class to fake a role """

    def __init__(self, id, name, guild, position):
        """ init a role with id, name, guild, position
        and MagicMock for state """
        role_data = {'id': id, 'name': name, 'position': position}
        super().__init__(data=role_data, guild=guild, state=MagicMock())


class FakeTextChannel(TextChannel):
    """ Class to fake a text channel """

    def __init__(self, name, guild, type, position):
        """ init a role with a user, a list of roles, a guild
        and MagicMock for state """
        channel_data = {
            'id': next(discord_id), 'name': name,
            'type': type, 'position': position}
        super().__init__(data=channel_data, guild=guild, state=MagicMock())


class FakeGuild(Guild):
    """ Class to fake a guild """

    def __init__(self, name, members, roles, channels, owner_id):
        """ init a guild with id, name,
        list of tuple for members (FakeUser, roles(list of name)),
        list of tuple for roles (name, position), a owner id
        and MagicMock for state """
        guild_data = {
            'id': next(discord_id), 'name': name, 'members': members,
            'channels': channels, 'roles': roles, 'owner_id': owner_id}
        super().__init__(data=guild_data, state=MagicMock())

    def _from_data(self, guild):
        """ override _from_data method to init just necessary properties
        -id -name -description -roles -members -owner -emojis -channels """
        self.id = int(guild['id'])
        self.name = guild.get('name')
        self.description = guild.get('description')
        self._roles = {}
        # add default role @everyone with the same id than the guild
        default_role = FakeRole(
            id=self.id, name='@everyone', guild=self, position=0)
        self._roles[default_role.id] = default_role
        # add roles
        name_id_roles = {}
        for name_pos in guild.get('roles', []):
            role = FakeRole(
                id=next(discord_id), name=name_pos[0], guild=self,
                position=name_pos[1])
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
            if name_type_pos[1] == 'TextChannel':
                self._add_channel(FakeTextChannel(
                    guild=self, name=name_type_pos[0],
                    type=0, position=name_type_pos[2]))
            # elif c_type == ChannelType.voice.value:
            #     self._add_channel(VoiceChannel(guild=self, data=c, state=self._state))
            # elif c_type == ChannelType.category.value:
            #     self._add_channel(CategoryChannel(guild=self, data=c, state=self._state))
            # elif c_type == ChannelType.store.value:
            #     self._add_channel(StoreChannel(guild=self, data=c, state=self._state))


class FakeContext(MagicMock):
    """ Mock for a context with a fake guild """

    spec_set = Context(message=MagicMock(), prefix=MagicMock())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
