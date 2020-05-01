from unittest.mock import MagicMock
from discord import CategoryChannel, TextChannel, VoiceChannel, StoreChannel
from .f_id import DISCORD_ID
from .f_permover import FakePermissionOverwrites


class FakeChannelData(dict):
    """Class to fake a channel data dict."""

    def __init__(self, **kwargs):
        """Init with keys id, name, position
        and permission_overwrites if there is role or member."""
        super().__init__()
        self.update(kwargs)
        del self['guild']
        self['id'] = next(DISCORD_ID)
        if self['roles'] or self['members']:
            self['permission_overwrites'] = FakePermissionOverwrites(
                self['roles'], self['members'])
        try:
            self['type'] = self.pop('c_type')
        except KeyError:
            pass


class FakeCategoryChannel(CategoryChannel):
    """Class to fake a categry channel."""

    def __init__(self, **kwargs):
        """Init with a FakeChannelData, a guild and MagicMock for state."""
        super().__init__(
            data=FakeChannelData(**kwargs),
            guild=kwargs['guild'], state=MagicMock())


class FakeTextChannel(TextChannel):
    """Class to fake a text channel."""

    def __init__(self, **kwargs):
        """Init with a FakeChannelData (add 'type' = (text->0 news->5)),
        a guild, and MagicMock for state"""
        super().__init__(
            data=FakeChannelData(**kwargs),
            guild=kwargs['guild'], state=MagicMock())


class FakeVoiceChannel(VoiceChannel):
    """Class to fake a voice channel."""

    def __init__(self, **kwargs):
        """Init with a FakeChannelData, a guild and MagicMock for state."""
        super().__init__(
            data=FakeChannelData(**kwargs),
            guild=kwargs['guild'], state=MagicMock())


class FakeStoreChannel(StoreChannel):
    """Class to fake a store channel."""

    def __init__(self, **kwargs):
        """Init with a FakeChannelData, a guild and MagicMock for state."""
        super().__init__(
            data=FakeChannelData(**kwargs),
            guild=kwargs['guild'], state=MagicMock())
