from .r_shapers import GuildEmbedTestResult, GuildShellTestResult


# BASE_RESULT -> {author(name: , icon_url), color, type}
BASE_RESULT = {'author': {
    'name': 'Full guild',
    'icon_url': 'https://cdn.discordapp.com/icons/6/icon.png.webp?size=1024'
    }, 'color': 1447446, 'type': 'rich'}


def get_full_embed_dict(embed_dict):
    """Return the full embed dict, dict to be updated + base."""
    embed_dict.update(BASE_RESULT)
    return embed_dict


def get_list_embed_dict(title, values, total):
    """Return embed dict {title, fields, footer} and updated with base."""
    return get_full_embed_dict({
        'title': title,
        'fields': [
            {'inline': True, 'name': 'ID', 'value': values[0]},
            {'inline': True, 'name': 'Name', 'value': values[1]}],
        'footer': {'text': f'Total: {total}'}})


# MAKE OBJS EMBED RESULTS -> MakeObjsEmbedTest expected results
O_RESULTS = {
    'list': get_list_embed_dict('Members', ('1\n0\n2', 'Pam\nPim\nPom'), '3'),
    'no_list': get_full_embed_dict({'title': 'No member'})
}

# GUILD RESULTS -> InfoGuildCommandsTest expected results
G_RESULTS = {
    'gld': get_full_embed_dict(GuildEmbedTestResult().add_title_stats),
    'own': get_list_embed_dict('Owner', ('0', 'Jean-Pierre'), '1'),
    'mem': get_full_embed_dict(GuildEmbedTestResult().add_title_objs),
    'rol': get_list_embed_dict('Roles', (
        '6\n7\n8', '@everyone\nadmin\nstaff'), '3'),
    'cat': get_list_embed_dict('Channel Categories', (
        '9\n10', '1st floor\n2nd floor'), '2'),
    'cha': get_list_embed_dict('Channels', (
        '17\n12\n16\n11\n13\n14\n15',
        'boss office\ninfo point\nmeeting room\nreception\nshop\nsnack\nstudio'
        ), '7'),
    'tcha': get_list_embed_dict('Text Channels', (
        '17\n16\n11', 'boss office\nmeeting room\nreception'), '3'),
    'vcha': get_list_embed_dict('Voice Channels', (
        '14\n15', 'snack\nstudio'), '2'),
    'ncha': get_list_embed_dict('News Channels', ('12', 'info point'), '1'),
    'scha': get_list_embed_dict('Store Channels', ('13', 'shop'), '1'),
    'emo': get_full_embed_dict({
        'title': 'Emojis', 'fields': GuildEmbedTestResult().add_emojis,
        'footer': {'text': 'Total: 4'}}),
    'shl': GuildShellTestResult().add_infos}
