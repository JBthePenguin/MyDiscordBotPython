from unittest.mock import MagicMock
from discord import Guild
from discord.enums import ChannelType
from .f_id import DISCORD_ID
from .f_role import FakeRole
from .f_member import FakeMember
from .f_channels import (
    FakeCategoryChannel, FakeTextChannel, FakeVoiceChannel, FakeStoreChannel)
from .f_emoji import FakeEmoji


class FakeGuild(Guild):
    """ Class to fake a guild. """

    def __init__(
            self, name, roles, members, categories, channels, emojis,
            description=None):
        """Init with id, name, description(default=None), list of tuple for:
        - members (FakeUser, list of roles's name),
        - roles (name, position, permissions(bool)),
        - categories channel (category name or None, name, position),
        - channels (category name or None, name, type, position,
            roles and members names lists to overwrite permission,
                or '@everyone' for roles to allow all members),
        a list of emojis' names.
        *** first FakeUser in the members list will be the owner ***"""
        guild_data = {
            'id': next(DISCORD_ID), 'name': name, 'roles': roles,
            'members': members, 'categories': categories, 'channels': channels,
            'emojis': emojis}
        super().__init__(data=guild_data, state=MagicMock())

    def get_c_members_roles(self, name_id_roles, roles, members):
        """With lists of names, return list for roles ids and members ids,
        that used to init FakeChannel with permission overwrites."""
        # roles
        if roles == '@everyone':
            c_roles = [self.default_role.id]
        else:
            c_roles = []
            for role_name in roles:
                c_roles.append(name_id_roles[role_name])
        # members
        c_members = []
        for member_name in members:
            c_members.append(self.get_member_named(member_name).id)
        return c_roles, c_members

    def _from_data(self, guild):
        """Override _from_data method (called at the end of Guild init)
        to set properties with our custom datas ->
        -id -name -description -icon -roles -members
        -owner -emojis -channels."""
        # id - name - description - icon
        self.id = int(guild['id'])
        self.name = guild.get('name')
        self.description = guild.get('description')
        self.icon = "icon.png"
        # roles
        self._roles = {}
        # add default role @everyone with the same id than the guild
        default_role = FakeRole(
            role_id=self.id, name='@everyone', guild=self, position=0,
            permissions=False)
        self._roles[default_role.id] = default_role
        # add roles
        name_id_roles = {}  # used to add members and channels
        for tup_role in guild.get('roles'):
            role = FakeRole(
                role_id=next(DISCORD_ID), name=tup_role[0], guild=self,
                position=tup_role[1], permissions=tup_role[2])
            self._roles[role.id] = role
            name_id_roles[role.name] = role.id
        # add members (with their roles)
        for tup_member in guild.get('members'):
            m_roles = []  # list of member's roles ids
            for role_name in tup_member[1]:
                m_roles.append(name_id_roles[role_name])
            member = FakeMember(user=tup_member[0], guild=self, roles=m_roles)
            member.name_id_update(tup_member[0])
            self._add_member(member)
        # add owner (the first in members list)
        self.owner_id = self.members[0].id
        # categories channels
        name_id_categories = {None: None}  # used to add channels
        for tup_category in guild.get('categories'):
            # roles and members ids lists to permission overwrite
            c_roles, c_members = self.get_c_members_roles(
                name_id_roles, tup_category[3], tup_category[4])
            category = FakeCategoryChannel(
                guild=self, parent_id=name_id_categories[tup_category[0]],
                name=tup_category[1], position=tup_category[2],
                roles=c_roles, members=c_members)
            self._add_channel(category)
            name_id_categories[category.name] = category.id
        # channels
        for tup_channel in guild.get('channels'):
            # roles and members ids lists to permission overwrite
            c_roles, c_members = self.get_c_members_roles(
                name_id_roles, tup_channel[4], tup_channel[5])
            # Create Channel
            if tup_channel[2] in (  # text or news
                    ChannelType.text.value, ChannelType.news.value):
                channel = FakeTextChannel(
                    guild=self, parent_id=name_id_categories[tup_channel[0]],
                    name=tup_channel[1], c_type=tup_channel[2],
                    position=tup_channel[3], roles=c_roles, members=c_members)
            elif tup_channel[2] == ChannelType.voice.value:  # voice
                channel = FakeVoiceChannel(
                    guild=self, parent_id=name_id_categories[tup_channel[0]],
                    name=tup_channel[1], position=tup_channel[3],
                    roles=c_roles, members=c_members)
            elif tup_channel[2] == ChannelType.store.value:  # store
                channel = FakeStoreChannel(
                    guild=self, parent_id=name_id_categories[tup_channel[0]],
                    name=tup_channel[1], position=tup_channel[3],
                    roles=c_roles, members=c_members)
            self._add_channel(channel)
        # add emojis
        self.emojis = tuple(
            FakeEmoji(name, self) for name in guild.get('emojis'))
