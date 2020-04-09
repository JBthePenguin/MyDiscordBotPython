# Configurations of commands -> {key: {'name': name, 'help': help text}}
def conf_dict(name, help):
    """ return a dict with the name of a command and his help text"""
    return {'name': name, 'help': help}


confs = {
    'shell': conf_dict('shell_info', 'Display infos in shell -> #shell_info'),
    'mem': conf_dict('all_mems', "All members -> #all_mems"),
    'rol': conf_dict('all_roles', "All roles -> #all_roles"),
    'cat': conf_dict('all_cats', "All categories's channel -> #all_cats"),
    'chan': conf_dict('all_chans', 'All channels -> #all_chans'),
    'rol_mem': conf_dict(
        'role_mems',
        'Members with a role-> #role_mems "role name or id"'),
    'cat_chan': conf_dict(
        'cat_chans',
        'Channels with a category-> #cat_chans "cat name or id"'),
    'chan_mem': conf_dict(
        'chan_mems',
        'Auth Members on chan-> #chan_mems "chan name or id"')}

# Error messages -> {name: message, ...}
error_msgs = {
    'no_exist': "{}: {} not exist", }  # {} -> obj field, value
