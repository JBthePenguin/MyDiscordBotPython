from aiounittest import AsyncTestCase
from discord.ext.commands import Cog
from ..guild import InfoGuildCommands
from .fakers import BOT, CONTEXT
from .results import InfoGuildCommandsTestResult


class InfoGuildCommandsTest(AsyncTestCase):
    """ Async Test case for cog InfoGuildCommands """

    def setUp(self):
        """ Init tests with cog and expected results """
        self.cog = InfoGuildCommands(BOT)
        self.result = InfoGuildCommandsTestResult()

    def test_init(self):
        """ assert after init is instance Cog """
        # cog = InfoGuildCommands(BOT)
        self.assertIsInstance(self.cog, Cog)

    async def test_guild(self):
        """ assert after guild command if send method is called once
        and if it's the good embed that's sended """
        await self.cog.guild.callback(self.cog, CONTEXT)
        CONTEXT.send.assert_called_once()
        args, kwargs = CONTEXT.send.call_args
        self.assertDictEqual(kwargs['embed'].to_dict(), self.result.guild)
        # print(kwargs['embed'].to_dict())
        # print('\n')
        # print(self.result.guild.to_dict())
