from unittest.mock import MagicMock
from discord import Emoji
from .f_id import DISCORD_ID


class FakeEmoji(Emoji):
    """Class to fake a emoji."""

    def __init__(self, name, guild):
        """Init with a id, a name, two boolean require_colons, managed (True),
        and MagicMock for state."""
        emoji_data = {
            'id': next(DISCORD_ID), 'name': name,
            'require_colons': True, 'managed': True}
        super().__init__(data=emoji_data, guild=guild, state=MagicMock())
