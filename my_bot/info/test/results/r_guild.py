from .r_shapers import GuildShellTestResult

# BASE_RESULT -> {author(name: , icon_url), color, type}
BASE_RESULT = {'author': {
    'name': 'Full guild',
    'icon_url': 'https://cdn.discordapp.com/icons/6/icon.png.webp?size=1024'
    }, 'color': 1447446, 'type': 'rich'}

# STATS FIELDS -> fields for all guild's stats
STATS_FIELDS = []
for name_value in [
        ('Members', '6'), ('Roles', '3'), ('Emojis', '4'),
        ('Channel Categories', '2'), ('Channels', '7'), ('Text Channels', '3'),
        ('Voice Channels', '2'), ('News Channels', '1'),
        ('Store Channels', '1')]:
    STATS_FIELDS.append(
        {'inline': True, 'name': name_value[0], 'value': name_value[1]})


def get_embed_dict(title, fields, footer_text):
    embed_dict = {
        'title': title, 'fields': fields, 'footer': {'text': footer_text}}
    embed_dict.update(BASE_RESULT)
    return embed_dict


def get_list_embed_dict(title, values, total):
    """Return an embed dict for a list of objs.
    -> {title, fields, footer} and updated with base."""
    if title == 'Emojis':
        name_one = '\u200b'
        name_two = '\u200b'
    else:
        name_one = 'ID'
        name_two = 'Name'
    fields = [
        {'inline': True, 'name': name_one, 'value': values[0]},
        {'inline': True, 'name': name_two, 'value': values[1]}]
    return get_embed_dict(title, fields, f'Total: {total}')


# GUILD RESULTS -> InfoGuildCommandsTest expected results
G_RESULTS = {
    'gld': get_embed_dict('id: 6', STATS_FIELDS, 'Owner: Jean-Pierre'),
    'own': get_list_embed_dict('Owner', ('0', 'Jean-Pierre'), '1'),
    'mem': get_list_embed_dict('Members', (
        '1\n3\n0\n2\n4\n5', 'Al\nBilly\nJean-Pierre\nJoe\nJohn\nMike'), '6'),
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
    'emo': get_list_embed_dict(
        'Emojis', (
            '<:bad:20> bad\n\n<:strong:21> strong',
            '<:cool:18> cool\n\n<:good:19> good'), '4'),
    'shl': GuildShellTestResult().add_infos}
