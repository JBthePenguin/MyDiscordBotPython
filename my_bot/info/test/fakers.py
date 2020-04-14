from unittest.mock import MagicMock
from discord import Guild, Member
from discord.ext.commands import Context


class FakeEmptyGuild(Guild):
    """ Mock for a context with a fake guild """

    def __init__(self):
        default_data = {
            'id': 10000,
            'name': 'Fake Guild',
            'icon_url': 'https://url.com/icon.png',}
            # 'region': 'Europe',
            # 'verification_level': 2,
            # 'default_notications': 1,
            # 'afk_timeout': 100,
            # 'icon': "icon.png",
            # 'banner': 'banner.png',
            # 'mfa_level': 1,
            # 'splash': 'splash.png',
            # 'system_channel_id': 464033278631084042,
            # 'description': 'mocking is fun',
            # 'max_presences': 10_000,
            # 'max_members': 100_000,
            # 'preferred_locale': 'UTC',
            # 'owner_id': 1,
            # 'afk_channel_id': 464033278631084042, }
        super().__init__(data=default_data, state=MagicMock())


class FakeMember(Member):
    """ Mock for a context with a fake guild """

    def __init__(self, data, guild):
        super().__init__(data=data, guild=guild, state=MagicMock())


fake_empty_guild = FakeEmptyGuild()
owner = FakeMember({'id': 1, 'user': 'lemon', 'roles': [1]}, fake_empty_guild)



class FakeFullGuild(Guild):
    """ Mock for a context with a fake guild """

    def __init__(self):
        default_data = {
            'id': 10001,
            'name': 'Fake Guild',
            'icon_url': 'https://url.com/icon.png',}
            # 'region': 'Europe',
            # 'verification_level': 2,
            # 'default_notications': 1,
            # 'afk_timeout': 100,
            # 'icon': "icon.png",
            # 'banner': 'banner.png',
            # 'mfa_level': 1,
            # 'splash': 'splash.png',
            # 'system_channel_id': 464033278631084042,
            # 'description': 'mocking is fun',
            # 'max_presences': 10_000,
            # 'max_members': 100_000,
            # 'preferred_locale': 'UTC',
            # 'owner_id': 1,
            # 'afk_channel_id': 464033278631084042, }
        print(owner.name)
        super().__init__(data=default_data, state=MagicMock())


class FakeContext(MagicMock):
    """ Mock for a context with a fake guild """

    spec_set = Context(message=MagicMock(), prefix=MagicMock())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
