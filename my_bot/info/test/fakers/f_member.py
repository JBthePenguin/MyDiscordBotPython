from unittest.mock import MagicMock
from discord import User, Member
from discord.enums import DefaultAvatar
from .f_id import DISCORD_ID


class FakeUser(User):
    """Class to fake a user."""

    def __init__(self, username):
        """Init with an id, a username, a bot, a discriminator, an avatar,
        and MagicMock for state."""
        user_data = {
            'id': next(DISCORD_ID), 'username': username, 'bot': False,
            'discriminator': username, 'avatar': str(DefaultAvatar)}
        super().__init__(data=user_data, state=MagicMock())


class FakeMember(Member):
    """Class to fake a member."""

    def __init__(self, user, guild, roles):
        """Init with a user, a guild, a list of roles ids
        and MagicMock for state."""
        mem_data = {
            'user': user, 'roles': roles,
            'joined_at': "2020-04-27T13:00:00.000000+00:00"}
        super().__init__(data=mem_data, guild=guild, state=MagicMock())

    def name_id_update(self, user):
        """Update id, name, bot, avatar, discriminator
        using the FakeUser's properties."""
        u = self._user
        modified = (
            user.id, user.name, user.bot,
            user.avatar, user.discriminator)
        u.id, u.name, u.bot, u.avatar, u.discriminator = modified

    @property
    def avatar_url(self):
        return 'https://url.com/avatar.png'
