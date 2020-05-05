from aiounittest import AsyncTestCase
from unittest.mock import Mock, patch
from discord.ext.commands import Bot
from ..guild import InfoGuildCommands
from .fakers import CONTEXT
from .results import G_RESULTS as RESULTS


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
        await self.assert_send_method(self.cog.guild, RESULTS['gld'])

    async def test_members(self):
        """Assert send method after members command."""
        await self.assert_send_method(self.cog.members, RESULTS['mem'])

    async def test_roles(self):
        """Assert send method after roles command."""
        await self.assert_send_method(self.cog.roles, RESULTS['rol'])

    async def test_categories(self):
        """Assert send method after categories command."""
        await self.assert_send_method(self.cog.categories, RESULTS['cat'])

    async def test_channels(self):
        """Assert send method after channels command."""
        await self.assert_send_method(self.cog.channels, RESULTS['cha'])

    async def test_text_channels(self):
        """Assert send method after text_channels command."""
        await self.assert_send_method(self.cog.text_channels, RESULTS['tcha'])

    async def test_voice_channels(self):
        """Assert send method after voice_channels command."""
        await self.assert_send_method(
            self.cog.voice_channels, RESULTS['vcha'])

    async def test_news_channels(self):
        """Assert send method after news_channels command."""
        await self.assert_send_method(
            self.cog.news_channels, RESULTS['ncha'])

    async def test_store_channels(self):
        """Assert send method after store_channels command."""
        await self.assert_send_method(
            self.cog.store_channels, RESULTS['scha'])

    async def test_emojis(self):
        """Assert send method after emojis command."""
        await self.assert_send_method(self.cog.emojis, RESULTS['emo'])

    async def test_shell_info(self):
        """Mock print function, assert if it,
        and the context send method is called once with the good string."""
        mock_print = Mock()
        with patch("builtins.print", mock_print):
            await self.cog.shell_info.callback(self.cog, self.ctx)
            mock_print.assert_called_once()
            guild_shell = mock_print.call_args[0][0]
            self.assertEqual(str(guild_shell), RESULTS['shl'])
            self.ctx.send.assert_called_once_with("Infos displayed in shell")
