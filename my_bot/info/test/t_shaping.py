from unittest import TestCase
from discord import Embed
from .fakers import FakeUser, FakeGuild, FakeMember
from .results import GuildEmbedTestResult
from ..shaping import GuildEmbed
from ..config import title_mem

# class Obj():
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name


class GuildEmbedTest(TestCase):
    """ Test case for class GuildEmbed """

    def setUp(self):
        """ Init tests with a GuildEmbed object  """
        self.embed_name = 'Guild Embed Test'
        self.embed_icon_url = "https://url.com/icon.png"
        self.result = GuildEmbedTestResult()

    def test_init(self):
        """ assert after init is instance Embed and the dict result """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        self.assertIsInstance(embed, Embed)
        self.assertDictEqual(embed.to_dict(), self.result.init_method)

    def test_add_stat(self):
        """ assert after add_stat if a field is added
        with a title and the number of ojs """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_stat(title_mem, ['a', 'b', 'c', 'd', 'e'])
        self.assertDictEqual(embed.to_dict(), self.result.add_stat)

    def test_add_title_stats(self):
        """ assert after add_title_stats if fields are added
        with the good title and the corresponding number of ojs for value """
        owner = FakeUser(username='Bill')
        roles = [('admin', 2, True), ('master', 1, False)]
        members = [
            (owner, []),
            (FakeUser(username='Joe'), ['admin']),
            (FakeUser(username='Al'), ['master']),
            (FakeUser(username='John'), []),
            (FakeUser(username='Jean-Pierre'), []), ]
        channels = [
            ('saloon', 'TextChannel', 3, '@everyone', []),
            ('public', 'News', 0, '@everyone', []),
            ('sheriff office', 'TextChannel', 1, [], ['Jean-Pierre']),
            ('school', 'TextChannel', 1, ['master'], []),
            ('souk', 'VoiceChannel', 0, '@everyone', [])]
        fake_guild = FakeGuild(
            name="Fake guild", roles=roles, members=members,
            channels=channels)
        # print(fake_guild.owner.roles)
        # print('\n')
        # print(fake_guild.id, fake_guild.name)
        # print('roles:', fake_guild.roles)
        # print(fake_guild.default_role)
        for member in fake_guild.members:
            print(member.id, member.name, member.roles)
        for channel in fake_guild.channels:
            print(channel.name, channel.type, len(channel.members))
        print('Owner:', fake_guild.owner.name)
        # embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        # embed.add_title_stats(fake_guild)
        # print(embed.to_dict())



# class MyTest(aiounittest.AsyncTestCase):
#
#     async def test_add_title_stats(self):
#         """ assert after add_title_stats if fields are added
#         with the good title and the corresponding number of ojs for value """
#         fake_guild = FakeGuild(data=guild_data)
#         channel = fake_guild.create_text_channel('cool-channel')
#         print(channel.id)
#         print(fake_guild.channels)
        # fake_context = FakeContext(guild=fake_guild)
        # fake_context.send("rtt")
        # fake_context.send.assert_called_once()
        # print(fake_context.guild.owner)
