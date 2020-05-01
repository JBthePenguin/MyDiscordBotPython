from unittest import TestCase
from aiounittest import AsyncTestCase
from discord.ext.commands import Cog
from ..components import InfoComponentsCommands, check_parameter
from .fakers import BOT, FULL_GUILD, CONTEXT
from .results import InfoComponentsCommandsTestResult


class CheckParameterTest(TestCase):
    """Test Case for check_parameter function.
    *** test with member of FakeGuild ***"""

    def assert_check_return(self, param, result, exist):
        """Assert if the good obj if exist, or message if not, is returned."""
        obj = check_parameter(
            param, FULL_GUILD.get_member, FULL_GUILD.get_member_named)
        if exist:
            self.assertEqual(obj.id, result[0])
            self.assertEqual(obj.name, result[1])
        else:
            self.assertEqual(obj, result)

    def test_exist_id(self):
        """Assert if check_parameter return the good obj."""
        self.assert_check_return('1', (1, 'Al'), True)

    def test_exist_name(self):
        """Assert if check_parameter return the good obj."""
        self.assert_check_return('Joe', (2, 'Joe'), True)

    def test_non_exist_id(self):
        """Assert if check_parameter return 'with id param not founded'."""
        self.assert_check_return('10', "with id 10 not founded.", False)

    def test_non_exist_name(self):
        """Assert if check_parameter return 'with name param not founded'."""
        self.assert_check_return('Polo', "with name Polo not founded.", False)


class InfoComponentsCommandsTest(AsyncTestCase):
    """Async Test case for cog InfoComponentsCommands."""
    cog = InfoComponentsCommands(BOT)
    result = InfoComponentsCommandsTestResult()
    maxDiff = None
    ctx = CONTEXT

    def setUp(self):
        """Init tests with a reset mock called count and args."""
        self.ctx.send.reset_mock()

    def test_init(self):
        """Assert after init is instance Cog, the number of commands,
        and if they have good name and help."""
        self.assertIsInstance(self.cog, Cog)
        commands = self.cog.get_commands()
        self.assertEqual(len(commands), 1)
        c_tuples = [(c.name, c.help) for c in commands]
        for i in range(len(commands)):
            self.assertTupleEqual(c_tuples[i], self.result.init_method[i])

    async def assert_send_method(self, command, param, result, exist):
        """"Call the command, assert if ctx.send is called once,
        and if the good embed or the not exist message is sended."""
        await command.callback(self.cog, self.ctx, param)
        self.ctx.send.assert_called_once()
        args, kwargs = self.ctx.send.call_args
        if exist:
            self.assertDictEqual(
                kwargs['embed'].to_dict(), result)
        else:
            self.assertEqual(args[0], result)

    async def test_member_id_exist(self):
        """Assert send method after member command with an exist id."""
        await self.assert_send_method(
            self.cog.member, '1', self.result.member['id'], True)

    async def test_member_name_exist(self):
        """Assert send method after member command with an exist name."""
        await self.assert_send_method(
            self.cog.member, 'Joe', self.result.member['name'], True)

    async def test_member_id_no_exist(self):
        """Assert send method after member command with a no exist id."""
        await self.assert_send_method(
            self.cog.member, '12', self.result.member['no_id'], False)

    async def test_member_name_no_exist(self):
        """Assert send method after member command with a no exist name."""
        await self.assert_send_method(
            self.cog.member, 'Tom', self.result.member['no_name'], False)
