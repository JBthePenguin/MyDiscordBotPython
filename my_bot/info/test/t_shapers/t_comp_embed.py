from unittest import TestCase
from discord import Embed
from ..fakers import FULL_GUILD
from ..results import ComponentEmbedTestResult
from ...shapers import ComponentEmbed


class ComponentEmbedTest(TestCase):
    """Test case for class ComponentEmbed."""
    result = ComponentEmbedTestResult()
    maxDiff = None

    def setUp(self):
        """Init tests with an embed."""
        self.embed = ComponentEmbed(
            3, 'Name', 1447446, 'https://url.com/icon.png')

    def test_init(self):
        """Assert after init is instance Embed,
        and if the dict result have id name desription color icon_url."""
        self.assertIsInstance(self.embed, Embed)
        self.assertDictEqual(self.embed.to_dict(), self.result.init_method)

    def test_add_list_in_field(self):
        """Assert if after add_list_in_field if infos are added correctly,
        *** test with a list of members name ***"""
        self.embed.add_list_in_field(
            [m.name for m in FULL_GUILD.members], 8, 'Members')
        self.assertDictEqual(
            self.embed.to_dict(), self.result.add_list_in_field)

    def test_add_auth_channels(self):
        """Assert if after add_auth_channels if infos are added correctly,
        *** test with a role without view permission on all channels ***"""
        self.embed.add_auth_channels(FULL_GUILD.get_role(8))
        self.assertDictEqual(
            self.embed.to_dict(), self.result.add_auth_channels)

    def test_add_member_infos(self):
        """Assert if after add_member_infos if infos are added correctly,
        - bot or human (if owner) - status - roles- auth channels - footer."""
        self.embed.add_member_infos(
            FULL_GUILD.get_member(2), FULL_GUILD.owner_id)
        self.assertDictEqual(
            self.embed.to_dict(), self.result.add_member_infos)

    def test_add_role_infos(self):
        """Assert if after add_role_infos if infos are added correctly,
        - position - members- auth channels - footer."""
        self.embed.add_role_infos(FULL_GUILD.get_role(8))
        self.assertDictEqual(self.embed.to_dict(), self.result.add_role_infos)
