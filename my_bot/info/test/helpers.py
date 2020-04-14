import unittest.mock
import discord
import itertools
from typing import Iterable, Optional
import collections


class HashableMixin(discord.mixins.EqualityComparable):
    """
    Mixin that provides similar hashing and equality functionality as discord.py's `Hashable` mixin.
    Note: discord.py`s `Hashable` mixin bit-shifts `self.id` (`>> 22`); to prevent hash-collisions
    for the relative small `id` integers we generally use in tests, this bit-shift is omitted.
    """

    def __hash__(self):
        return self.id


class ColourMixin:
    """A mixin for Mocks that provides the aliasing of color->colour like discord.py does."""

    @property
    def color(self) -> discord.Colour:
        return self.colour

    @color.setter
    def color(self, color: discord.Colour) -> None:
        self.colour = color


class CustomMockMixin:
    """
    Provides common functionality for our custom Mock types.
    The `_get_child_mock` method automatically returns an AsyncMock for coroutine methods of the mock
    object. As discord.py also uses synchronous methods that nonetheless return coroutine objects, the
    class attribute `additional_spec_asyncs` can be overwritten with an iterable containing additional
    attribute names that should also mocked with an AsyncMock instead of a regular MagicMock/Mock. The
    class method `spec_set` can be overwritten with the object that should be uses as the specification
    for the mock.
    Mock/MagicMock subclasses that use this mixin only need to define `__init__` method if they need to
    implement custom behavior.
    """

    child_mock_type = unittest.mock.MagicMock
    discord_id = itertools.count(0)
    spec_set = None
    additional_spec_asyncs = None

    def __init__(self, **kwargs):
        name = kwargs.pop('name', None)  # `name` has special meaning for Mock classes, so we need to set it manually.
        super().__init__(spec_set=self.spec_set, **kwargs)

        if self.additional_spec_asyncs:
            self._spec_asyncs.extend(self.additional_spec_asyncs)

        if name:
            self.name = name

    def _get_child_mock(self, **kw):
        """
        Overwrite of the `_get_child_mock` method to stop the propagation of our custom mock classes.
        Mock objects automatically create children when you access an attribute or call a method on them. By default,
        the class of these children is the type of the parent itself. However, this would mean that the children created
        for our custom mock types would also be instances of that custom mock type. This is not desirable, as attributes
        of, e.g., a `Bot` object are not `Bot` objects themselves. The Python docs for `unittest.mock` hint that
        overwriting this method is the best way to deal with that.
        This override will look for an attribute called `child_mock_type` and use that as the type of the child mock.
        """
        _new_name = kw.get("_new_name")
        if _new_name in self.__dict__['_spec_asyncs']:
            return unittest.mock.AsyncMock(**kw)

        _type = type(self)
        if issubclass(_type, unittest.mock.MagicMock) and _new_name in unittest.mock._async_method_magics:
            # Any asynchronous magic becomes an AsyncMock
            klass = unittest.mock.AsyncMock
        else:
            klass = self.child_mock_type

        if self._mock_sealed:
            attribute = "." + kw["name"] if "name" in kw else "()"
            mock_name = self._extract_mock_name() + attribute
            raise AttributeError(mock_name)

        return klass(**kw)
# Create a guild instance to get a realistic Mock of `discord.Guild`
guild_data = {
    'id': 1,
    'name': 'guild',
    'region': 'Europe',
    'verification_level': 2,
    'default_notications': 1,
    'afk_timeout': 100,
    'icon': "icon.png",
    'banner': 'banner.png',
    'mfa_level': 1,
    'splash': 'splash.png',
    'system_channel_id': 464033278631084042,
    'description': 'mocking is fun',
    'max_presences': 10_000,
    'max_members': 100_000,
    'preferred_locale': 'UTC',
    'owner_id': 1,
    'afk_channel_id': 464033278631084042,}
guild_instance = discord.Guild(data=guild_data, state=unittest.mock.MagicMock())

# Create a Role instance to get a realistic Mock of `discord.Role`
role_data = {'name': 'role', 'id': 1}
role_instance = discord.Role(guild=guild_instance, state=unittest.mock.MagicMock(), data=role_data)


class MockRole(CustomMockMixin, unittest.mock.Mock, ColourMixin, HashableMixin):
    """
    A Mock subclass to mock `discord.Role` objects.
    Instances of this class will follow the specifications of `discord.Role` instances. For more
    information, see the `MockGuild` docstring.
    """
    spec_set = role_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {
            'id': next(self.discord_id),
            'name': 'role',
            'position': 1,
            'colour': discord.Colour(0xdeadbf),
            'permissions': discord.Permissions(),
        }
        super().__init__(**collections.ChainMap(kwargs, default_kwargs))

        if isinstance(self.colour, int):
            self.colour = discord.Colour(self.colour)

        if isinstance(self.permissions, int):
            self.permissions = discord.Permissions(self.permissions)

        if 'mention' not in kwargs:
            self.mention = f'&{self.name}'

    def __lt__(self, other):
        """Simplified position-based comparisons similar to those of `discord.Role`."""
        return self.position < other.position


class MockGuild(CustomMockMixin, unittest.mock.Mock, HashableMixin):
    """
    A `Mock` subclass to mock `discord.Guild` objects.
    A MockGuild instance will follow the specifications of a `discord.Guild` instance. This means
    that if the code you're testing tries to access an attribute or method that normally does not
    exist for a `discord.Guild` object this will raise an `AttributeError`. This is to make sure our
    tests fail if the code we're testing uses a `discord.Guild` object in the wrong way.
    One restriction of that is that if the code tries to access an attribute that normally does not
    exist for `discord.Guild` instance but was added dynamically, this will raise an exception with
    the mocked object. To get around that, you can set the non-standard attribute explicitly for the
    instance of `MockGuild`:
    >>> guild = MockGuild()
    >>> guild.attribute_that_normally_does_not_exist = unittest.mock.MagicMock()
    In addition to attribute simulation, mocked guild object will pass an `isinstance` check against
    `discord.Guild`:
    >>> guild = MockGuild()
    >>> isinstance(guild, discord.Guild)
    True
    For more info, see the `Mocking` section in `tests/README.md`.
    """
    spec_set = guild_instance

    def __init__(self, roles: Optional[Iterable[MockRole]] = None, **kwargs) -> None:
        default_kwargs = {'id': next(self.discord_id), 'members': []}
        super().__init__(**collections.ChainMap(kwargs, default_kwargs))

        self.roles = [MockRole(name="@everyone", position=1, id=0)]
        if roles:
            self.roles.extend(roles)
