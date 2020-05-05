# ### Guild Embed
# BASE_RESULT -> {author(name: , icon_url), color, type}
BASE_RESULT = {'author': {
    'name': 'Full guild',
    'icon_url': 'https://cdn.discordapp.com/icons/6/icon.png.webp?size=1024'
    }, 'color': 1447446, 'type': 'rich'}


def get_embed_dict(title, values=None, total=None):
    """Return an embed dict for all guild's stats or a list of objs.
    -> {title, fields, footer} and updated with base result."""
    # fiels config and footer text
    if title == 'id: 6':  # Guild
        tups_name_val = [
            ('Members', '6'), ('Roles', '3'), ('Emojis', '4'),
            ('Channel Categories', '2'), ('Channels', '7'),
            ('Text Channels', '3'), ('Voice Channels', '2'),
            ('News Channels', '1'), ('Store Channels', '1')]
        footer_text = 'Owner: Jean-Pierre'
    else:
        if title == 'Emojis':  # Emojis
            tups_name_val = [('\u200b', values[0]), ('\u200b', values[1])]
        else:  # members, roles,...
            tups_name_val = [('ID', values[0]), ('Name', values[1])]
        footer_text = f'Total: {total}'
    # fields list
    fields = []
    for name_val in tups_name_val:
        fields.append(
            {'inline': True, 'name': name_val[0], 'value': name_val[1]})
    # updated embed dict with a base for all results
    embed_dict = {
        'title': title, 'fields': fields, 'footer': {'text': footer_text}}
    embed_dict.update(BASE_RESULT)
    return embed_dict


# ### Guild shell
# G_STRING -> string with all guild's infos
G_STRING = '\n'.join([
    '\n\n########## Guild ##########',
    '- 6 - Full guild',
    '\n########## Owner ##########',
    '- 0 - Jean-Pierre',
    '\n########## 6 Members ##########',
    '- 1 - Al',
    '- 3 - Billy',
    '- 0 - Jean-Pierre',
    '- 2 - Joe',
    '- 4 - John',
    '- 5 - Mike',
    '\n########## 3 Roles ##########',
    '- 6 - @everyone',
    '- 7 - admin',
    '- 8 - staff',
    '\n########## 4 Emojis ##########',
    '- <:cool:18> cool - <:good:19> good - <:bad:20> bad',
    '- <:strong:21> strong',
    '\n########## 2 Channel Categories ##########',
    '- 9 - 1st floor',
    '- 10 - 2nd floor',
    '\n########## 7 Channels ##########',
    '- 17 - boss office',
    '- 12 - info point',
    '- 16 - meeting room',
    '- 11 - reception',
    '- 13 - shop',
    '- 14 - snack',
    '- 15 - studio',
    '\n########## 3 Text Channels ##########',
    '- 17 - boss office',
    '- 16 - meeting room',
    '- 11 - reception',
    '\n########## 2 Voice Channels ##########',
    '- 14 - snack',
    '- 15 - studio',
    '\n########## 1 News Channels ##########',
    '- 12 - info point',
    '\n########## 1 Store Channels ##########',
    '- 13 - shop',
    "\n\n########## CHANNELS BY CATEGORIES ##########",
    '\n##### No channel category #####',
    '### 1 Text Channels',
    '- 11 - reception',
    '### 1 News Channels',
    '- 12 - info point',
    '\n##### 1st floor #####',
    '### 2 Voice Channels',
    '- 14 - snack',
    '- 15 - studio',
    '### 1 Store Channels',
    '- 13 - shop',
    '\n##### 2nd floor #####',
    '### 2 Text Channels',
    '- 17 - boss office',
    '- 16 - meeting room\n'])


# GUILD RESULTS -> InfoGuildCommandsTest expected results
G_RESULTS = {
    'gld': get_embed_dict('id: 6'),
    # 'own': get_embed_dict('Owner', ('0', 'Jean-Pierre'), '1'),
    'mem': get_embed_dict('Members', (
        '1\n3\n0\n2\n4\n5', 'Al\nBilly\nJean-Pierre\nJoe\nJohn\nMike'), '6'),
    'rol': get_embed_dict('Roles', (
        '6\n7\n8', '@everyone\nadmin\nstaff'), '3'),
    'cat': get_embed_dict('Channel Categories', (
        '9\n10', '1st floor\n2nd floor'), '2'),
    'cha': get_embed_dict('Channels', (
        '17\n12\n16\n11\n13\n14\n15',
        'boss office\ninfo point\nmeeting room\nreception\nshop\nsnack\nstudio'
        ), '7'),
    'tcha': get_embed_dict('Text Channels', (
        '17\n16\n11', 'boss office\nmeeting room\nreception'), '3'),
    'vcha': get_embed_dict('Voice Channels', (
        '14\n15', 'snack\nstudio'), '2'),
    'ncha': get_embed_dict('News Channels', ('12', 'info point'), '1'),
    'scha': get_embed_dict('Store Channels', ('13', 'shop'), '1'),
    'emo': get_embed_dict(
        'Emojis', (
            '<:bad:20> bad\n\n<:strong:21> strong',
            '<:cool:18> cool\n\n<:good:19> good'), '4'),
    'shl': G_STRING}
