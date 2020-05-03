from unittest import TestCase
from discord import Guild
from ..results import GuildShellTestResult
from ..fakers import FULL_GUILD
from ...shapers import GuildShell


class GuildShellTest(TestCase):
    """Test case for class GuildShell."""
    result = GuildShellTestResult()

    def setUp(self):
        """Init tests with a guild_shell."""
        self.guild_shell = GuildShell(FULL_GUILD)

    def test_init(self):
        """Assert after init if property infos is instance str,
        and if property guild is instance Guild."""
        self.assertIsInstance(self.guild_shell.infos, str)
        self.assertIsInstance(self.guild_shell.guild, Guild)

    def assert_add_list(self, l_titles, objs, result):
        """Assert after add_list if the good title,
        and the good infos are added."""
        self.guild_shell.add_list(l_titles, objs)
        self.assertEqual(self.guild_shell.infos, result)

    def test_add_guild(self):
        """Assert after add guild infos to the string."""
        self.assert_add_list(
            ('Guild', 'guild'), [self.guild_shell.guild],
            self.result.add_list['guild'])

    def test_add_owner(self):
        """Assert after add owner infos to the string."""
        self.assert_add_list(
            ('Owner', 'owner'), [self.guild_shell.guild.owner],
            self.result.add_list['owner'])

    def test_add_objs(self):
        """Assert after add objs (here members) infos to the string."""
        self.assert_add_list(
            ('Members', 'member'), self.guild_shell.guild.members,
            self.result.add_list['objs'])

    def test_add_empty_list(self):
        """Assert after add empty list (here members) infos to the string."""
        self.assert_add_list(
            ('Members', 'member'), [], '\n########## No member ##########\n')

    def test_add_emojis(self):
        """Assert after add_emojis if the list of emojis,
        with str() repr and name are added to the string, 3 by line."""
        self.guild_shell.add_emojis(self.guild_shell.guild.emojis)
        self.assertEqual(self.guild_shell.infos, self.result.add_emojis)

    def assert_add_type_chans(self, channels, result):
        """Assert after add_type_chans if the good title,
        and the sorted list of channels (voice for this test)."""
        self.guild_shell.add_type_chans(channels, 'Voice Channels')
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

    def test_empty_cats_chans(self):
        """Assert after add empty cats_chans infos to string."""
        self.assert_add_cats_chans([], '')

    def test_add_infos(self):
        """Assert after add_infos if all infos are added correctly."""
        self.guild_shell.add_infos()
        self.assertEqual(self.guild_shell.infos, self.result.add_infos)
