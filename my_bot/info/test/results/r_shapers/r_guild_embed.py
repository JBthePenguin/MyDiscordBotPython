# GuildEmbedTest expected results
G_EMBED_RESULTS = {
    'init': {'author': {
        'name': 'Guild Embed Test',
        'icon_url': 'https://u.com/ic.png'}, 'color': 1447446, 'type': 'rich'},
    # 'stat': [{'inline': True, 'name': 'Members', 'value': '5'}],
    # 'tstats': {
    #     'title': 'id: 6', 'footer': {'text': 'Owner: Jean-Pierre'}, 'fields': [
    #         {'inline': True, 'name': 'Members', 'value': '6'},
    #         {'inline': True, 'name': 'Roles', 'value': '3'},
    #         {'inline': True, 'name': 'Emojis', 'value': '4'},
    #         {'inline': True, 'name': 'Channel Categories', 'value': '2'},
    #         {'inline': True, 'name': 'Channels', 'value': '7'},
    #         {'inline': True, 'name': 'Text Channels', 'value': '3'},
    #         {'inline': True, 'name': 'Voice Channels', 'value': '2'},
    #         {'inline': True, 'name': 'News Channels', 'value': '1'},
    #         {'inline': True, 'name': 'Store Channels', 'value': '1'}]},
    'tobjs': {
        'title': 'Members', 'footer': {'text': 'Total: 6'}, 'fields': [
            {'inline': True, 'name': 'ID', 'value': '1\n3\n0\n2\n4\n5'},
            {
                'inline': True, 'name': 'Name',
                'value': 'Al\nBilly\nJean-Pierre\nJoe\nJohn\nMike'}]},
    'eobjs': 'No member',
    'emos': [{
        'inline': True, 'name': '\u200b',
        'value': '<:bad:20> bad\n\n<:strong:21> strong'}, {
        'inline': True, 'name': '\u200b',
        'value': '<:cool:18> cool\n\n<:good:19> good'}]}
