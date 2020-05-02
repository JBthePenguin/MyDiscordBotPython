from unittest.mock import MagicMock
from discord import Role
from discord.permissions import Permissions
from datetime import datetime


class FakeRole(Role):
    """Class to fake a role."""

    def __init__(self, role_id, name, guild, position, permissions):
        """Init with an id, a name, a guild, a position,
        permissions (true -> add all permissions -> same as owner),
        and MagicMock for state.
        *** @everyone have same id than guild ***"""
        role_data = {'id': role_id, 'name': name, 'position': position}
        if permissions is True:
            role_data['permissions'] = Permissions.all().value
        super().__init__(data=role_data, guild=guild, state=MagicMock())

    @property
    def created_at(self):
        """Overwrite created at property to return a default value"""
        return datetime.strptime("2020-04-27 15:30", "%Y-%m-%d %H:%M")
