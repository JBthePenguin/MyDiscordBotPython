from unittest import TestCase
from discord import Embed
from ..results import GuildEmbedTestResult
from ..fakers import FULL_GUILD
from ...shapers import GuildEmbed


class GuildEmbedTest(TestCase):
    """Test case for class GuildEmbed."""
    result = GuildEmbedTestResult()
    maxDiff = None

    def setUp(self):
        """Init tests with an embed."""
        self.embed = GuildEmbed('Guild Embed Test', "https://url.com/icon.png")

    def test_init(self):
        """Assert after init is instance Embed,
        and if the dict result have the author name and icon_url."""
        self.assertIsInstance(self.embed, Embed)
        self.assertDictEqual(self.embed.to_dict(), self.result.init_method)

    def test_add_stat(self):
        """Assert after add_stat if a field is added,
        with good name and number of objs."""
        self.embed.add_stat('Members', ['a', 'b', 'c', 'd', 'e'])
        self.assertListEqual(
            self.embed.to_dict()['fields'], self.result.add_stat)

    def assert_add_title_foo(self, result):
        """Assert if in embed there is the good title and footer,
        if fields are added with the good name and value."""
        embed_dict = self.embed.to_dict()
        self.assertEqual(embed_dict['title'], result['title'])
        self.assertListEqual(embed_dict['fields'], result['fields'])
        self.assertDictEqual(embed_dict['footer'], result['footer'])

    def test_add_title_stats(self):
        """Assert after add_title_stats if there is the good title and footer,
        if fields are added with the good name and number of objs for value."""
        self.embed.add_title_stats(FULL_GUILD)
        self.assert_add_title_foo(self.result.add_title_stats)

    def test_add_title_objs(self):
        """Assert after add_title_objs if there is the good title and footer,
        if fields with names 'id' 'name' are added,
        and for each value, the lists of ids and names sorted by name."""
        self.embed.add_title_objs('mem', FULL_GUILD.members)
        self.assert_add_title_foo(self.result.add_title_objs)

    def test_add_empty_objs(self):
        """Assert after add empty objs if there is the good title and footer,
        if fields with 'no member'.
        *** test with members ***"""
        self.embed.add_title_objs('mem', [])
        self.assertEqual(self.embed.to_dict()['title'], 'No member')

    def test_add_emojis(self):
        """Assert after add_emojis if 2 fields without names are added,
        and for each value, the list of emojis separated in 2 parts,
        with str() repr and name."""
        self.embed.add_emojis(FULL_GUILD.emojis)
        self.assertListEqual(
            self.embed.to_dict()['fields'], self.result.add_emojis)
