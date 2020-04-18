from unittest import TestCase
from discord import Embed
from discord.enums import ChannelType
from .fakers import FULL_GUILD
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
        """ assert after init is instance Embed and
        if the dict result have the author name and icon_url"""
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        self.assertIsInstance(embed, Embed)
        self.assertDictEqual(embed.to_dict(), self.result.init_method)

    def test_add_stat(self):
        """ assert after add_stat if a field is added
        with a title (name) and the number of ojs """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_stat(title_mem, ['a', 'b', 'c', 'd', 'e'])
        self.assertListEqual(embed.to_dict()['fields'], self.result.add_stat)

    def test_add_title_stats(self):
        """ assert after add_title_stats if fields are added
        with the good title and the corresponding number of ojs for value """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_title_stats(FULL_GUILD)
        self.assertListEqual(
            embed.to_dict()['fields'], self.result.add_title_stats)

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
