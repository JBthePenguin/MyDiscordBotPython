from unittest import TestCase
from aiounittest import AsyncTestCase
from unittest.mock import Mock, patch
from discord.ext.commands import Cog
from ..guild import InfoGuildCommands, make_objs_embed
from ..shaping import GuildEmbed
from ..config import GUILD_TITLES as titles
from .fakers import BOT, CONTEXT
from .results import InfoGuildCommandsTestResult, MakeObjsEmbedTestResult


class MakeObjsEmbedTest(TestCase):
    """Test Case for make_objs_embed function.
    *** test with members of FakeGuild ***"""
    result = MakeObjsEmbedTestResult()
    maxDiff = None

    def assert_list(self, m_list, result):
        """Assert if make_objs_embed return the good embed."""
        embed = make_objs_embed(
            'Guild Embed Test', 'https://url.com/icon.png',
            titles.mem, m_list)
        self.assertIsInstance(embed, GuildEmbed)
        self.assertDictEqual(embed.to_dict(), result)

    def test_empty_list(self):
        """Assert with an empty list."""
        self.assert_list([], self.result.empty_list)

    def test_not_empty_list(self):
        """Assert with a list of members."""
        self.assert_list(CONTEXT.guild.members, self.result.not_empty_list)


class InfoGuildCommandsTest(AsyncTestCase):
    """Async Test case for cog InfoGuildCommands."""
    cog = InfoGuildCommands(BOT)
    result = InfoGuildCommandsTestResult()
    maxDiff = None

    def setUp(self):
        """Init tests with a reset mock called count and args."""
        CONTEXT.send.reset_mock()

    def test_init(self):
        """Assert after init is instance Cog, the number of commands,
        and if they have good name and help."""
        self.assertIsInstance(self.cog, Cog)
        commands = self.cog.get_commands()
        self.assertEqual(len(commands), 12)
        c_tuples = [(c.name, c.help) for c in commands]
        for i in range(len(commands)):
            self.assertTupleEqual(c_tuples[i], self.result.init_method[i])

    async def assert_send_method(self, method, result):
        """Assert if send method is called and if the good embed is sended."""
        await method.callback(self.cog, CONTEXT)
        CONTEXT.send.assert_called_once()
        kwargs = CONTEXT.send.call_args[1]
        self.assertDictEqual(kwargs['embed'].to_dict(), result)

    async def test_guild(self):
        """Assert send method after guild command."""
        await self.assert_send_method(self.cog.guild, self.result.guild)

    async def test_owner(self):
        """Assert send method after owner command."""
        await self.assert_send_method(self.cog.owner, self.result.owner)

    async def test_members(self):
        """Assert send method after members command."""
        await self.assert_send_method(self.cog.members, self.result.members)

    async def test_roles(self):
        """Assert send method after roles command."""
        await self.assert_send_method(self.cog.roles, self.result.roles)

    async def test_categories(self):
        """Assert send method after categories command."""
        await self.assert_send_method(
            self.cog.categories, self.result.categories)

    async def test_channels(self):
        """Assert send method after channels command."""
        await self.assert_send_method(self.cog.channels, self.result.channels)

    async def test_text_channels(self):
        """Assert send method after text_channels command."""
        await self.assert_send_method(
            self.cog.text_channels, self.result.text_channels)

    async def test_voice_channels(self):
        """Assert send method after voice_channels command."""
        await self.assert_send_method(
            self.cog.voice_channels, self.result.voice_channels)

    async def test_news_channels(self):
        """Assert send method after news_channels command."""
        await self.assert_send_method(
            self.cog.news_channels, self.result.news_channels)

    async def test_store_channels(self):
        """Assert send method after store_channels command."""
        await self.assert_send_method(
            self.cog.store_channels, self.result.store_channels)

    async def test_emojis(self):
        """Assert send method after emojis command."""
        await self.assert_send_method(
            self.cog.emojis, self.result.emojis)

    async def test_shell_info(self):
        """Mock print function, assert if it,
        and the context send method is called once with the good string."""
        mock_print = Mock()
        with patch("builtins.print", mock_print):
            await self.cog.shell_info.callback(self.cog, CONTEXT)
            mock_print.assert_called_once_with(self.result.shell_info)
            CONTEXT.send.assert_called_once_with("Infos displayed in shell")
