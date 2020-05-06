from .t_shapers import GuildEmbedTest, GuildShellTest, ComponentEmbedTest
from .t_guild import InfoGuildCommandsTest
from .t_components import CheckParameterTest, InfoComponentsCommandsTest
from .t_config import ConfCommandsTest


ALL_TESTS_CASE = [
    GuildEmbedTest, GuildShellTest, ComponentEmbedTest,
    InfoGuildCommandsTest, InfoComponentsCommandsTest, CheckParameterTest,
    ConfCommandsTest]
