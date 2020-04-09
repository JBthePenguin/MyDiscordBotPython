def conf_dict(name, help):
    """ return a dict with the name of a command and his help text"""
    return {'name': name, 'help': help}


# Configurations of commands -> {key: {'name': name, 'help': help text}}
confs = {
    'shell': conf_dict('shell_info', 'Display infos in shell -> #shell_info'),
    'mem': conf_dict('members', "All team's members-> #members"),
    'rol': conf_dict('roles', "All team's roles-> #roles"),
    'chan': conf_dict('channels', 'All channels by category-> #channels'),
    'rol_mem': conf_dict(
        'role_members',
        'Members with a role-> #role_members "role name or id"'),
    'chan_mem': conf_dict(
        'chan_members',
        'Auth Members on chan-> #chan_members "chan name or id"')}
