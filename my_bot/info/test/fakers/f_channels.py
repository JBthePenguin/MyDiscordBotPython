from unittest.mock import MagicMock
from discord import CategoryChannel, TextChannel, VoiceChannel, StoreChannel
from .f_id import DISCORD_ID
from .f_permover import FakePermissionOverwrites


class FakeChannelData(dict):
    """Class to fake a channel data dict."""

    def __init__(self, parent_id, name, position, roles, members, c_type=None):
        """Init with keys id, name, position
        and permission_overwrites if there is role or member."""
        super().__init__()
        self['id'] = next(DISCORD_ID)
        self['parent_id'] = parent_id
        self['name'] = name
        self['position'] = position
        if roles or members:
            self['permission_overwrites'] = FakePermissionOverwrites(
                roles, members)
        if c_type is not None:
            self['type'] = c_type


class FakeCategoryChannel(CategoryChannel):
    """Class to fake a categry channel."""

    def __init__(self, **kwargs):
        """Init with a FakeChannelData, a guild and MagicMock for state."""
        super().__init__(
            data=FakeChannelData(
                kwargs['parent_id'], kwargs['name'], kwargs['position'],
                kwargs['roles'], kwargs['members']),
            guild=kwargs['guild'], state=MagicMock())


class FakeTextChannel(TextChannel):
    """Class to fake a text channel."""

    def __init__(self, **kwargs):
        """Init with a FakeChannelData (add 'type' = (text->0 news->5)),
        a guild, and MagicMock for state"""
        super().__init__(
            data=FakeChannelData(
                kwargs['parent_id'], kwargs['name'], kwargs['position'],
                kwargs['roles'], kwargs['members'], kwargs['c_type']),
            guild=kwargs['guild'], state=MagicMock())


class FakeVoiceChannel(VoiceChannel):
    """Class to fake a voice channel."""

    def __init__(self, **kwargs):
        """Init with a FakeChannelData, a guild and MagicMock for state."""
        super().__init__(
            data=FakeChannelData(
                kwargs['parent_id'], kwargs['name'], kwargs['position'],
                kwargs['roles'], kwargs['members']),
            guild=kwargs['guild'], state=MagicMock())


class FakeStoreChannel(StoreChannel):
    """Class to fake a store channel."""

    def __init__(self, **kwargs):
        """Init with a FakeChannelData, a guild and MagicMock for state."""
        super().__init__(
            data=FakeChannelData(
                kwargs['parent_id'], kwargs['name'], kwargs['position'],
                kwargs['roles'], kwargs['members']),
            guild=kwargs['guild'], state=MagicMock())
