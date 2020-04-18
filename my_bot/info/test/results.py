class GuildEmbedTestResult():
    """ class with GuildEmbedTest expected result   """

    @property
    def init_method(self):
        """ return the result expected for test_init"""
        return {
            'author': {
                'name': 'Guild Embed Test',
                'icon_url': 'https://url.com/icon.png'},
            'color': 1447446,
            'type': 'rich'}

    @property
    def add_stat(self):
        """ return the result expected for test_add_stat"""
        return [{'inline': True, 'name': 'Members', 'value': '5'}]

    @property
    def add_title_stats(self):
        """ return the result expected for test_add_title_stats """
        return [
            {'inline': True, 'name': 'Members', 'value': '6'},
            {'inline': True, 'name': 'Roles', 'value': '3'},
            {'inline': True, 'name': 'Emojis', 'value': '4'},
            {'inline': True, 'name': 'Channel Categories', 'value': '2'},
            {'inline': True, 'name': 'Channels', 'value': '7'},
            {'inline': True, 'name': 'Text Channels', 'value': '3'},
            {'inline': True, 'name': 'Voice Channels', 'value': '2'},
            {'inline': True, 'name': 'News Channels', 'value': '1'},
            {'inline': True, 'name': 'Store Channels', 'value': '1'}]
