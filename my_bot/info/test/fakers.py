from unittest.mock import MagicMock
from discord import Guild, User, Member
from discord.ext.commands import Context
import itertools


discord_id = itertools.count(0)


class FakeUser(User):
    """ Mock for a user """

    def __init__(self, name):
        user_data = {
            'id': next(discord_id), 'username': name,
            'discriminator': name, 'avatar': str(discord_id)}
        super().__init__(data=user_data, state=MagicMock())


class FakeMember(Member):
    """ Mock for a member """

    def __init__(self, user, guild):
        mem_data = {'user': user, 'roles': []}
        mem_guild = guild
        super().__init__(data=mem_data, guild=mem_guild, state=MagicMock())

    def name_id_update(self, user):
        u = self._user
        modified = (user.id, user.name, user.avatar, user.discriminator)
        u.id, u.name, u.avatar, u.discriminator = modified


class FakeGuild(Guild):
    """ Mock for a guild """

    def __init__(self, name, members, owner_id):
        super().__init__(data={
            'id': next(discord_id), 'name': name,
            'members': members, 'owner_id': owner_id}, state=MagicMock())

    def _from_data(self, guild):
        # according to Stan, this is always available even
        # if the guild is unavailable
        # I don't have this guarantee when someone updates the guild.
        self.name = guild.get('name')
        self.id = int(guild['id'])
        self._roles = {}
        # for r in guild.get('roles', []):
        #     role = Role(guild=self, data=r, state=state)
        #     self._roles[role.id] = role
        self.emojis = guild.get('emojis', [])
        self.description = guild.get('description')
        # add members
        for mdata in guild.get('members', []):
            member = FakeMember(user=mdata, guild=self)
            member.name_id_update(mdata)
            self._add_member(member)
        # add owner
        self.owner_id = guild.get('owner_id')


class FakeContext(MagicMock):
    """ Mock for a context with a fake guild """

    spec_set = Context(message=MagicMock(), prefix=MagicMock())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
