from aiounittest import AsyncTestCase
from discord.ext.commands import Cog
from ..components import InfoComponentsCommands
from .fakers import BOT, FULL_GUILD, CONTEXT
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

    async def assert_send_method(self, method, result, id_name, not_exist):
        """ reset mock called count and args, and assert if
        send method is called once and if the good embed or
        the not exist message is sended
        *** test with exist id and name, with not exist id and name *** """
        # id exist
        CONTEXT.send.reset_mock()
        await method.callback(self.cog, CONTEXT, id_name[0])
        CONTEXT.send.assert_called_once()
        args, kwargs = CONTEXT.send.call_args
        # self.assertDictEqual(kwargs['embed'].to_dict(), result['id'])
        # name exist
        CONTEXT.send.reset_mock()
        await method.callback(self.cog, CONTEXT, id_name[1])
        CONTEXT.send.assert_called_once()
        args, kwargs = CONTEXT.send.call_args
        print(kwargs['embed'].to_dict())
        # self.assertDictEqual(kwargs['embed'].to_dict(), result['name'])
        # id not exist
        CONTEXT.send.reset_mock()
        await method.callback(self.cog, CONTEXT, not_exist[0])
        CONTEXT.send.assert_called_once()
        args, kwargs = CONTEXT.send.call_args
        self.assertEqual(args[0], result['no_id'])
        # name not exist
        CONTEXT.send.reset_mock()
        await method.callback(self.cog, CONTEXT, not_exist[1])
        CONTEXT.send.assert_called_once()
        args, kwargs = CONTEXT.send.call_args
        self.assertEqual(args[0], result['no_name'])

    async def test_member(self):
        """ assert send method after member command """
        await self.assert_send_method(
            self.cog.member, self.result.member,
            ("1", "Joe"), ("12", "Walter"))
