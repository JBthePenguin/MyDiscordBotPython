from unittest import TestCase
from aiounittest import AsyncTestCase
from discord.ext.commands import Cog
from ..components import InfoComponentsCommands, check_parameter
from .fakers import BOT, FULL_GUILD, CONTEXT
from .results import InfoComponentsCommandsTestResult


class CheckParameterTest(TestCase):
    """Test Case for check_parameter function.
    *** test with member of FakeGuild ***"""

    def test_exist_id(self):
        """Assert if check_parameter return the good obj."""
        obj = check_parameter(
            '1', FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        self.assertEqual(obj.id, 1)
        self.assertEqual(obj.name, 'Al')

    def test_exist_name(self):
        """Assert if check_parameter return the good obj."""
        obj = check_parameter(
            'Joe', FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        self.assertEqual(obj.id, 2)
        self.assertEqual(obj.name, 'Joe')

    def test_non_exist_id(self):
        """Assert if check_parameter return 'with id param not founded'."""
        obj = check_parameter(
            '10', FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        self.assertEqual(obj, "with id 10 not founded.")

    def test_non_exist_name(self):
        """Assert if check_parameter return 'with name param not founded'."""
        obj = check_parameter(
            'Polo', FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        self.assertEqual(obj, "with name Polo not founded.")


class InfoComponentsCommandsTest(AsyncTestCase):
    """Async Test case for cog InfoComponentsCommands."""

    def setUp(self):
        """Init tests with cog and expected results."""
        self.cog = InfoComponentsCommands(BOT)
        self.result = InfoComponentsCommandsTestResult()
        self.maxDiff = None

    def test_init(self):
        """Assert after init is instance Cog, the number of commands,
        and if they have good name and help."""
        self.assertIsInstance(self.cog, Cog)
        commands = self.cog.get_commands()
        self.assertEqual(len(commands), 1)
        c_tuples = [(c.name, c.help) for c in commands]
        for i in range(len(commands)):
            self.assertTupleEqual(c_tuples[i], self.result.init_method[i])

    async def assert_send_called(self, method, param, exist):
        """"Reset mock called count and args, call method,
        assert if ctx.send is called once,
        and return the embed dict or the not founded message sended."""
        CONTEXT.send.reset_mock()
        await method.callback(self.cog, CONTEXT, param)
        CONTEXT.send.assert_called_once()
        args, kwargs = CONTEXT.send.call_args
        if exist:
            return kwargs['embed'].to_dict()
        return args[0]

    async def assert_send_method(self, method, result, id_name, not_exist):
        """Assert if the good embed or the not exist message is sended.
        *** test with exist id and name, with not exist id and name ***"""
        # id and name exist
        values = [(id_name[0], result['id']), (id_name[1], result['name'])]
        for v in values:
            self.assertDictEqual(
                await self.assert_send_called(method, v[0], True), v[1])
        # id and name not exist
        values = [
            (not_exist[0], result['no_id']), (not_exist[1], result['no_name'])]
        for v in values:
            self.assertEqual(
                await self.assert_send_called(method, v[0], False), v[1])

    async def test_member(self):
        """Assert send method after member command."""
        await self.assert_send_method(
            self.cog.member, self.result.member,
            ("1", "Joe"), ("12", "Walter"))
