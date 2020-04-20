from aiounittest import AsyncTestCase
from discord.ext.commands import Cog
from ..guild import InfoGuildCommands
from ..shaping import GuildEmbed
from ..config import GUILD_COMMANDS as coms
from .fakers import BOT, CONTEXT
from .results import InfoGuildCommandsTestResult


class InfoGuildCommandsTest(AsyncTestCase):
    """ Async Test case for cog InfoGuildCommands """

    def setUp(self):
        """ Init tests with cog and expected results """
        self.cog = InfoGuildCommands(BOT)
        self.result = InfoGuildCommandsTestResult()
        self.maxDiff = None

    def test_init(self):
        """ assert after init is instance Cog, the number of commands
        and if they have good name and help """
        self.assertIsInstance(self.cog, Cog)
        commands = self.cog.get_commands()
        self.assertEqual(len(commands), 12)
        c_tuples = [(c.name, c.help) for c in commands]
        for i in range(len(commands)):
            self.assertTupleEqual(c_tuples[i], self.result.init_method[i])

    def assert_send_method(self, result):
        """ assert if send method is called once,
        if the good embed is sended and reset mock called count and args"""
        CONTEXT.send.assert_called_once()
        args, kwargs = CONTEXT.send.call_args
        self.assertDictEqual(kwargs['embed'].to_dict(), result)
        # print('\n')
        # print(kwargs['embed'].to_dict())

    async def test_guild(self):
        """ assert send method after guild command """
        CONTEXT.send.reset_mock()
        await self.cog.guild.callback(self.cog, CONTEXT)
        self.assert_send_method(self.result.guild)

    def test_make_objs_embed(self):
        """ assert if make_objs_embed return the good embed """
        embed = self.cog.make_objs_embed(
            'Guild Embed Test', 'https://url.com/icon.png',
            coms.mem.conf_embed, CONTEXT.guild.members)
        self.assertIsInstance(embed, GuildEmbed)
        self.assertDictEqual(embed.to_dict(), self.result.make_objs_embed)

    async def test_owner(self):
        """ assert send method after owner command """
        CONTEXT.send.reset_mock()
        await self.cog.owner.callback(self.cog, CONTEXT)
        self.assert_send_method(self.result.owner)

    async def test_members(self):
        """ assert send method after members command """
        CONTEXT.send.reset_mock()
        await self.cog.members.callback(self.cog, CONTEXT)
        self.assert_send_method(self.result.members)

    async def test_roles(self):
        """ assert send method after roles command """
        CONTEXT.send.reset_mock()
        await self.cog.roles.callback(self.cog, CONTEXT)
        self.assert_send_method(self.result.roles)

    async def test_categories(self):
        """ assert send method after categories command """
        CONTEXT.send.reset_mock()
        await self.cog.categories.callback(self.cog, CONTEXT)
        self.assert_send_method(self.result.categories)

    async def test_channels(self):
        """ assert send method after channels command """
        CONTEXT.send.reset_mock()
        await self.cog.channels.callback(self.cog, CONTEXT)
        self.assert_send_method(self.result.channels)

    async def test_text_channels(self):
        """ assert send method after text_channels command """
        CONTEXT.send.reset_mock()
        await self.cog.text_channels.callback(self.cog, CONTEXT)
        self.assert_send_method(self.result.text_channels)
