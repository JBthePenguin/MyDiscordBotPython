from unittest import TestCase
from aiounittest import AsyncTestCase
from unittest.mock import Mock, patch
from discord.ext.commands import Bot
from ..guild import InfoGuildCommands, make_objs_embed
from ..shapers import GuildEmbed
from .fakers import CONTEXT
from .results import MakeObjsEmbedTestResult, GUILD_RESULTS


class MakeObjsEmbedTest(TestCase):
    """Test Case for make_objs_embed function.
    *** test with members of FakeGuild ***"""
    result = MakeObjsEmbedTestResult()
    maxDiff = None

    def assert_list(self, m_list, result):
        """Assert if make_objs_embed return the good embed."""
        embed = make_objs_embed(
            'Guild Embed Test', 'https://url.com/icon.png',
            'mem', m_list)
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
    cog = InfoGuildCommands(Bot(command_prefix='#'))
    maxDiff = None
    ctx = CONTEXT

    def setUp(self):
        """Init tests with a reset mock called count and args."""
        self.ctx.send.reset_mock()

    async def assert_send_method(self, method, result):
        """Assert if send method is called and if the good embed is sended."""
        await method.callback(self.cog, self.ctx)
        self.ctx.send.assert_called_once()
        kwargs = self.ctx.send.call_args[1]
        self.assertDictEqual(kwargs['embed'].to_dict(), result)

    async def test_guild(self):
        """Assert send method after guild command."""
        await self.assert_send_method(self.cog.guild, GUILD_RESULTS['gld'])
        # await self.assert_send_method(self.cog.guild, self.result.guild)

    async def test_owner(self):
        """Assert send method after owner command."""
        await self.assert_send_method(self.cog.owner, GUILD_RESULTS['own'])

    async def test_members(self):
        """Assert send method after members command."""
        await self.assert_send_method(self.cog.members, GUILD_RESULTS['mem'])

    async def test_roles(self):
        """Assert send method after roles command."""
        await self.assert_send_method(self.cog.roles, GUILD_RESULTS['rol'])

    async def test_categories(self):
        """Assert send method after categories command."""
        await self.assert_send_method(
            self.cog.categories, GUILD_RESULTS['cat'])

    async def test_channels(self):
        """Assert send method after channels command."""
        await self.assert_send_method(self.cog.channels, GUILD_RESULTS['cha'])

    async def test_text_channels(self):
        """Assert send method after text_channels command."""
        await self.assert_send_method(
            self.cog.text_channels, GUILD_RESULTS['tcha'])

    async def test_voice_channels(self):
        """Assert send method after voice_channels command."""
        await self.assert_send_method(
            self.cog.voice_channels, GUILD_RESULTS['vcha'])

    async def test_news_channels(self):
        """Assert send method after news_channels command."""
        await self.assert_send_method(
            self.cog.news_channels, GUILD_RESULTS['ncha'])

    async def test_store_channels(self):
        """Assert send method after store_channels command."""
        await self.assert_send_method(
            self.cog.store_channels, GUILD_RESULTS['scha'])

    async def test_emojis(self):
        """Assert send method after emojis command."""
        await self.assert_send_method(
            self.cog.emojis, GUILD_RESULTS['emo'])

    async def test_shell_info(self):
        """Mock print function, assert if it,
        and the context send method is called once with the good string."""
        mock_print = Mock()
        with patch("builtins.print", mock_print):
            await self.cog.shell_info.callback(self.cog, self.ctx)
            mock_print.assert_called_once_with(GUILD_RESULTS['shl'])
            self.ctx.send.assert_called_once_with("Infos displayed in shell")
