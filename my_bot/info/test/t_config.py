from unittest import TestCase
from discord.ext.commands import Cog, Bot
from ..guild import InfoGuildCommands
from ..components import InfoComponentsCommands
from .results import CONF_RESULTS as RESULTS


class ConfCommandsTest(TestCase):
    """Test Case for commands's configuration"""
    maxDiff = None

    def assert_cog(self, cog_class, n_commands, results):
        """Assert after init is instance Cog, the number of commands,
        and if they have good name and help."""
        cog = cog_class(Bot(command_prefix='#'))
        self.assertIsInstance(cog, Cog)
        commands = cog.get_commands()
        self.assertEqual(len(commands), n_commands)
        for i, result in enumerate(results):
            self.assertTupleEqual((commands[i].name, commands[i].help), result)

    def test_cog_guild(self):
        """Assert cog InfoGuildCommands."""
        self.assert_cog(InfoGuildCommands, 11, RESULTS['gld'])

    def test_cog_components(self):
        """Assert cog InfoComponentsCommands."""
        self.assert_cog(InfoComponentsCommands, 1, RESULTS['comp'])
