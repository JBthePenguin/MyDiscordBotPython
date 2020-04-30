from unittest import TestCase
from discord import Embed, Guild
from .fakers import FULL_GUILD
from .results import (
    GuildEmbedTestResult, GuildShellTestResult, ComponentEmbedTestResult)
from ..shaping import GuildEmbed, GuildShell, ComponentEmbed
from ..config import GUILD_TITLES as titles


class GuildEmbedTest(TestCase):
    """Test case for class GuildEmbed."""

    def setUp(self):
        """Init tests with name and icon url to used with a GuildEmbed object,
        and expected results."""
        self.embed_name = 'Guild Embed Test'
        self.embed_icon_url = "https://url.com/icon.png"
        self.result = GuildEmbedTestResult()
        self.maxDiff = None

    def test_init(self):
        """Assert after init is instance Embed,
        and if the dict result have the author name and icon_url."""
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        self.assertIsInstance(embed, Embed)
        self.assertDictEqual(embed.to_dict(), self.result.init_method)

    def test_add_stat(self):
        """Assert after add_stat if a field is added,
        with good name and number of objs."""
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_stat(titles.mem, ['a', 'b', 'c', 'd', 'e'])
        self.assertListEqual(embed.to_dict()['fields'], self.result.add_stat)

    def test_add_title_stats(self):
        """Assert after add_title_stats if there is the good title and footer,
        if fields are added with the good name and number of objs for value."""
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_title_stats(FULL_GUILD)
        self.assertEqual(
            embed.to_dict()['title'], self.result.add_title_stats['title'])
        self.assertListEqual(
            embed.to_dict()['fields'], self.result.add_title_stats['fields'])
        self.assertDictEqual(
            embed.to_dict()['footer'], self.result.add_title_stats['footer'])

    def test_add_title_objs(self):
        """Assert after add_title_objs if there is the good title and footer,
        if fields with names 'id' 'name' are added,
        and for each value, the lists of ids and names sorted by name."""
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_title_objs(titles.mem, FULL_GUILD.members)
        self.assertEqual(
            embed.to_dict()['title'], self.result.add_title_objs['title'])
        self.assertListEqual(
            embed.to_dict()['fields'], self.result.add_title_objs['fields'])
        self.assertDictEqual(
            embed.to_dict()['footer'], self.result.add_title_objs['footer'])
        # with an empty list
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_title_objs(titles.mem, [])
        self.assertEqual(embed.to_dict()['title'], 'No member')

    def test_add_emojis(self):
        """Assert after add_emojis if 2 fields without names are added,
        and for each value, the list of emojis separated in 2 parts,
        with str() repr and name."""
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_emojis(FULL_GUILD.emojis)
        self.assertListEqual(embed.to_dict()['fields'], self.result.add_emojis)


class GuildShellTest(TestCase):
    """Test case for class GuildShell."""
    result = GuildShellTestResult()

    def setUp(self):
        """Init tests with the expected results."""
        self.guild_shell = GuildShell(FULL_GUILD)

    def test_init(self):
        """Assert after init if property infos is instance str,
        and if property guild is instance Guild."""
        self.assertIsInstance(self.guild_shell.infos, str)
        self.assertIsInstance(self.guild_shell.guild, Guild)

    def assert_add_list(self, title, objs, result):
        """Assert after add_list if the good title,
        and the good infos are added."""
        self.guild_shell.add_list(title, objs)
        self.assertEqual(self.guild_shell.infos, result)

    def test_add_guild(self):
        """Assert after add guild infos to the string."""
        self.assert_add_list(
            titles.gld, [self.guild_shell.guild],
            self.result.add_list['guild'])

    def test_add_owner(self):
        """Assert after add owner infos to the string."""
        self.assert_add_list(
            titles.own, [self.guild_shell.guild.owner],
            self.result.add_list['owner'])

    def test_add_objs(self):
        """Assert after add objs (here members) infos to the string."""
        self.assert_add_list(
            titles.mem, self.guild_shell.guild.members,
            self.result.add_list['objs'])

    def test_add_empty_list(self):
        """Assert after add empty list (here members) infos to the string."""
        self.assert_add_list(
            titles.mem, [], '\n########## No member ##########\n')

    def test_add_emojis(self):
        """Assert after add_emojis if the list of emojis,
        with str() repr and name are added to the string, 3 by line."""
        self.guild_shell.add_emojis(self.guild_shell.guild.emojis)
        self.assertEqual(self.guild_shell.infos, self.result.add_emojis)

    def assert_add_type_chans(self, channels, result):
        """Assert after add_type_chans if the good title,
        and the sorted list of channels (voice for this test)."""
        self.guild_shell.add_type_chans(channels, titles.vcha)
        self.assertEqual(self.guild_shell.infos, result)

    def test_add_chans(self):
        """Assert after add chans infos to the string."""
        self.assert_add_type_chans(
            self.guild_shell.guild.voice_channels, self.result.add_type_chans)

    def test_empty_chans(self):
        """Assert after add empty list of chans infos to the string."""
        self.assert_add_type_chans([], '')

    def assert_add_cats_chans(self, cat_chans, result):
        """Assert after add_cats_chans if the good titles,
        and the sorted list of channels sorted by category, type and name."""
        self.guild_shell.add_cats_chans(self.guild_shell.guild.by_category())
        self.assertEqual(self.guild_shell.infos, self.result.add_cats_chans)

    def test_cats_chans(self):
        """Assert after add cats_chans infos to string."""
        self.assert_add_cats_chans(
            self.guild_shell.guild.by_category(), self.result.add_cats_chans)
        # guild_shell.add_cats_chans(guild_shell.guild.by_category())
        # self.assertEqual(guild_shell.infos, self.result.add_cats_chans)

    def test_empty_cats_chans(self):
        """Assert after add empty cats_chans infos to string."""
        self.assert_add_cats_chans([], '')

    def test_add_infos(self):
        """Assert after add_infos if all infos are added correctly."""
        # guild_shell = GuildShell(FULL_GUILD)
        self.guild_shell.add_infos()
        self.assertEqual(self.guild_shell.infos, self.result.add_infos)


class ComponentEmbedTest(TestCase):
    """Test case for class ComponentEmbed."""
    result = ComponentEmbedTestResult()
    maxDiff = None

    def setUp(self):
        """Init tests with expected results."""
        self.embed = ComponentEmbed(
            3, 'Name', 1447446, 'https://url.com/icon.png')

    def test_init(self):
        """Assert after init is instance Embed,
        and if the dict result have id name desription color icon_url."""
        self.assertIsInstance(self.embed, Embed)
        self.assertDictEqual(self.embed.to_dict(), self.result.init_method)

    def test_add_member_infos(self):
        """Assert if after add_member_infos if infos are added correctly,
        - bot or human - status - roloes- auth channels - footer."""
        self.embed.add_member_infos(FULL_GUILD.get_member(2))
        self.assertDictEqual(
            self.embed.to_dict(), self.result.add_member_infos)
