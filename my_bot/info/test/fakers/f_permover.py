from discord.permissions import PermissionOverwrite


class FakePermissionOverwrites(list):
    """Class to fake a permission overwrites list."""

    def __init__(self, roles, members):
        """Init with read and send messages permissions for specific,
        roles and members. *** used for argument in init FakeChannel ***
        -> [{'id': role or member id, 'type': 'role' or 'member',
        'allow': value, 'deny': value}, ...]"""
        super().__init__()
        permission = PermissionOverwrite(
            read_messages=True, send_messages=True).pair()
        allow, deny = permission[0].value, permission[1].value
        for role_id in roles:
            self.append(
                {"id": role_id, "type": 'role', 'allow': allow, 'deny': deny})
        for mem_id in members:
            self.append(
                {"id": mem_id, "type": 'member', 'allow': allow, 'deny': deny})
