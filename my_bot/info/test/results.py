class GuildEmbedTestResult():
    """ class with GuildEmbedTest expected result   """

    def __init__(self):
        self.init_method = {
            'author': {
                'name': 'Guild Embed Test',
                'icon_url': 'https://url.com/icon.png'},
            'color': 1447446,
            'type': 'rich'}
        self.add_stat = {
            'author': self.init_method['author'],
            'fields': [{'inline': True, 'name': 'Members', 'value': '5'}],
            'color': self.init_method['color'],
            'type': self.init_method['type']}
