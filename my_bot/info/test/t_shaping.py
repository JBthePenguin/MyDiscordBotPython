from unittest import TestCase
from datetime import datetime
from discord import Embed, Guild
from .fakers import FakeUser, FakeGuild, FakeMember
from .results import GuildEmbedTestResult
from ..shaping import GuildEmbed
from ..config import title_mem

# class Obj():
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name


class GuildEmbedTest(TestCase):
    """ Test case for class GuildEmbed """

    def setUp(self):
        """ Init tests with a GuildEmbed object  """
        self.embed_name = 'Guild Embed Test'
        self.embed_icon_url = "https://url.com/icon.png"
        self.result = GuildEmbedTestResult()

    def test_init(self):
        """ assert after init is instance Embed and the dict result """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        self.assertIsInstance(embed, Embed)
        self.assertDictEqual(embed.to_dict(), self.result.init_method)

    def test_add_stat(self):
        """ assert after add_stat if a field is added
        with a title and the number of ojs """
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_stat(title_mem, ['a', 'b', 'c', 'd', 'e'])
        self.assertDictEqual(embed.to_dict(), self.result.add_stat)

    def test_add_title_stats(self):
        """ assert after add_title_stats if fields are added
        with the good title and the corresponding number of ojs for value """
        # fake_guild = FakeGuild(name="Fake guild", owner=FakeUser(name='Joe'), members=[FakeUser(name='Bill'), FakeUser(name='Jean-Pierre')])
        # fake_owner = FakeMember(user=FakeUser(name='Joe'), guild=fake_guild)
        # fake_guild.add_owner(fake_owner)
        # fake_member = FakeMember(user=FakeUser(name='Bill'), guild=fake_guild)
        # nfake_member = FakeMember(user=FakeUser(name='Jean-Pierre'), guild=fake_guild)
        # print(fake_member.id)
        # print(fake_member.name)
        # print(fake_guild.members)
        # fake_guild.add_owner(fake_owner)
        # print(fake_guild.owner.name)
        # print(fake_guild.owner_id)
        user_one = FakeUser(name='Bill')
        print(user_one.name)
        print(user_one.id)
        user_two = FakeUser(name='Jean-Pierre')
        print(user_two.name)
        print(user_two.id)
        fake_guild = FakeGuild(name="Fake guild", members=[user_one, user_two], owner_id=0)
        # print(fake_guild.name)
        # print(fake_guild._members)
        # print(fake_guild.members)
        for member in fake_guild.members:
            print(member.id)
            print(member.name)
        # # print(fake_guild.get_member(0))
        # self.assertIsInstance(fake_guild, Guild)
        # fake_member = FakeMember(joined_at=str(datetime.now), guild=fake_guild)
        # owner = FakeMember({'user': 'lemon', 'roles': [1]}, fake_guild)
        # fake_guild.owner = owner
        # print(fake_guild.name)
        print(fake_guild.owner.name)
        embed = GuildEmbed(self.embed_name, self.embed_icon_url)
        embed.add_title_stats(fake_guild)
        print(embed.to_dict())
        # embed.add_stat(title_mem, ['a', 'b', 'c', 'd', 'e'])
        # self.assertDictEqual(embed.to_dict(), self.result.add_stat)


# class MyTest(aiounittest.AsyncTestCase):
#
#     async def test_add_title_stats(self):
#         """ assert after add_title_stats if fields are added
#         with the good title and the corresponding number of ojs for value """
#         fake_guild = FakeGuild(data=guild_data)
#         channel = fake_guild.create_text_channel('cool-channel')
#         print(channel.id)
#         print(fake_guild.channels)
        # fake_context = FakeContext(guild=fake_guild)
        # fake_context.send("rtt")
        # fake_context.send.assert_called_once()
        # print(fake_context.guild.owner)
