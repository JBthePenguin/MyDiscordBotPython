# Configurations of commands -> {key: {'name': name, 'help': help text}}
def conf_dict(name, help):
    """ return a dict with the name of a command and his help text"""
    return {'name': name, 'help': help}


confs = {
    'shl': conf_dict('shell', 'Display infos in shell -> #shell'),
    'mem': conf_dict('mems', "All members -> #mems"),
    'rol': conf_dict('roles', "All roles -> #roles"),
    'cat': conf_dict('cats', "All channel's categories -> #cats"),
    'cha': conf_dict('chans', 'All channels -> #chans'),
    'tcha': conf_dict('tchans', 'All text channels -> #tchans'),
    'vcha': conf_dict('vchans', 'All voice channels -> #vchans'),
    'rolmem': conf_dict(
        'role_mems',
        'Members with a role-> #role_mems "role name or id"'),
    'catcha': conf_dict(
        'cat_chans',
        'Channels with a category-> #cat_chans "cat name or id"'),
    'chamem': conf_dict(
        'chan_mems',
        'Auth Members on chan-> #chan_mems "chan name or id"')}

# Error messages -> {name: message, ...}
error_msgs = {
    'no_exist': "{}: {} not exist",  # {} -> obj field, value
    'empty_list': "{}: No {}", }  # {} -> location, obj type
