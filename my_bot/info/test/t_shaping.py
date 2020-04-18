from unittest import TestCase
from discord import Embed, Guild
from .fakers import FULL_GUILD
from .results import GuildEmbedTestResult, GuildShellTestResult
from ..shaping import GuildEmbed, GuildShell
from ..config import title_mem


class GuildEmbedTest(TestCase):
    """ Test case for class GuildEmbed """

    def setUp(self):
        """ Init tests with name and icon url to used with a GuildEmbed object
        and expected results """
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
        with good name and number of ojs """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_stat(title_mem, ['a', 'b', 'c', 'd', 'e'])
        self.assertListEqual(embed.to_dict()['fields'], self.result.add_stat)

    def test_add_title_stats(self):
        """ assert after add_title_stats if there is the good title and footer,
        if fields are added with the good name
        and the corresponding number of ojs for value """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_title_stats(FULL_GUILD)
        self.assertEqual(
            embed.to_dict()['title'], self.result.add_title_stats['title'])
        self.assertListEqual(
            embed.to_dict()['fields'], self.result.add_title_stats['fields'])
        self.assertDictEqual(
            embed.to_dict()['footer'], self.result.add_title_stats['footer'])

    def test_add_title_objs(self):
        """ assert after add_title_objs if there is the good title and footer,
        if fields with names 'id' 'name' are added
        and for each value, the lists of ids and names sorted by name """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_title_objs(title_mem, FULL_GUILD.members)
        self.assertEqual(
            embed.to_dict()['title'], self.result.add_title_objs['title'])
        self.assertListEqual(
            embed.to_dict()['fields'], self.result.add_title_objs['fields'])
        self.assertDictEqual(
            embed.to_dict()['footer'], self.result.add_title_objs['footer'])
        # with an empty list
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_title_objs(title_mem, [])
        self.assertEqual(embed.to_dict()['title'], 'No member')

    def test_add_emojis(self):
        """ assert after add_emojis if 2 fields without names are added
        and for each value, the list of emojis separated in 2 parts
        with str() repr and name """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_emojis(FULL_GUILD.emojis)
        self.assertListEqual(embed.to_dict()['fields'], self.result.add_emojis)


class GuildShellTest(TestCase):
    """ Test case for class GuildShell """

    def setUp(self):
        """ Init tests with the expected results """
        self.result = GuildShellTestResult()

    def test_init(self):
        """ assert after init if property infos is instance str and
        if property guild is instance Guild """
        guild_shell = GuildShell(FULL_GUILD)
        self.assertIsInstance(guild_shell.infos, str)
        self.assertIsInstance(guild_shell.guild, Guild)

    def test_add_list(self):
        """ assert after add_list if the good title
        and the sorted list of infos are added to the string """
        guild_shell = GuildShell(FULL_GUILD)
        guild_shell.add_list(title_mem, guild_shell.guild.members)
        self.assertEqual(guild_shell.infos, self.result.add_list)
        # with empty list
        guild_shell = GuildShell(FULL_GUILD)
        guild_shell.add_list(title_mem, [])
        self.assertEqual(
            guild_shell.infos, '\n########## No member ##########\n')

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
