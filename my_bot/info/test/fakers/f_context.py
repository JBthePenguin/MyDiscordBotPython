from unittest.mock import MagicMock
from asyncio import coroutine
from discord.ext.commands import Context


class FakeContext(Context):
    """Class to fake a Context."""

    def __init__(self, guild):
        """Init with MagicMock for message and prefix, add guild
        and Mock the send method."""
        super().__init__(message=MagicMock(), prefix=MagicMock())
        self.guild = guild
        self.send = MagicMock(side_effect=coroutine(lambda embed: None))
