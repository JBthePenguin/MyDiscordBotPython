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

    def test_init(self):
        """ assert after init is instance Cog, the number of commands
        and if they have good name and help """
        self.assertIsInstance(self.cog, Cog)
        commands = self.cog.get_commands()
        self.assertEqual(len(commands), 12)
        c_tuples = [(c.name, c.help) for c in commands]
        for i in range(len(commands)):
            self.assertTupleEqual(c_tuples[i], self.result.init_method[i])

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

    def test_make_objs_embed(self):
        """ assert if make_objs_embed return the good embed """
        embed = self.cog.make_objs_embed(
            'Guild Embed Test', 'https://url.com/icon.png',
            coms.mem.conf_embed, CONTEXT.guild.members)
        self.assertIsInstance(embed, GuildEmbed)
        self.assertDictEqual(embed.to_dict(), self.result.make_objs_embed)
