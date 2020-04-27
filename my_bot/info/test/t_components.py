from aiounittest import AsyncTestCase
from discord.ext.commands import Cog
from ..components import InfoComponentsCommands
from .fakers import BOT, FULL_GUILD
from .results import InfoComponentsCommandsTestResult


class InfoComponentsCommandsTest(AsyncTestCase):
    """ Async Test case for cog InfoComponentsCommands """

    def setUp(self):
        """ Init tests with cog and expected results """
        self.cog = InfoComponentsCommands(BOT)
        self.result = InfoComponentsCommandsTestResult()
        self.maxDiff = None

    def test_init(self):
        """ assert after init is instance Cog, the number of commands
        and if they have good name and help """
        self.assertIsInstance(self.cog, Cog)
        commands = self.cog.get_commands()
        self.assertEqual(len(commands), 1)
        c_tuples = [(c.name, c.help) for c in commands]
        for i in range(len(commands)):
            self.assertTupleEqual(c_tuples[i], self.result.init_method[i])

    def test_check_parameter(self):
        """ assert if check_parameter return the good obj
        or no obj with this param founded
        *** test with member of FakeGuild"""
        # with an exist id
        obj = self.cog.check_parameter(
            '1', FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.name, 'Al')
        # with an exit name
        obj = self.cog.check_parameter(
            'Joe', FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        self.assertEqual(obj.id, 2)
        self.assertEqual(obj.name, 'Joe')
        # with an non exist id
        obj = self.cog.check_parameter(
            '10', FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        self.assertEqual(obj, "with id 10 not founded.")
        # with an non exist name
        obj = self.cog.check_parameter(
            'Polo', FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        self.assertEqual(obj, "with name Polo not founded.")
