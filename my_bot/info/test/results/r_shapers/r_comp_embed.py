class ComponentEmbedTestResult():
    """Class with ComponentEmbedTest expected result."""

    @property
    def init_method(self):
        """Return the result expected for test_init."""
        return {
            'title': "Name",
            'author': {
                'name': 'id: 3',
                'icon_url': 'https://url.com/icon.png'},
            'color': 1447446,
            'type': 'rich'}

    @property
    def add_list_in_field(self):
        """Return the result expected for test_add_list_in_field."""
        embed_dict = {
            'fields': [
                {
                    'inline': False, 'name': 'Members',
                    'value': 'Al - Billy - Jean-Pierre - Joe - John - Mike'}]}
        embed_dict.update(self.init_method)
        return embed_dict

    @property
    def add_auth_channels(self):
        """Return the result expected for test_add_auth_channels."""
        embed_dict = {
            'fields': [
                {
                    'inline': False, 'name': 'Channels allowed to view',
                    'value': 'snack - studio'}]}
        embed_dict.update(self.init_method)
        return embed_dict

    @property
    def add_member_infos(self):
        """Return the result expected for test_add_member_infos."""
        embed_dict = {
            'footer': {'text': 'Member since'},
            'fields': [
                {
                    'inline': False, 'name': 'Roles',
                    'value': '@everyone - staff'},
                {
                    'inline': False, 'name': 'Channels allowed to view',
                    'value': ''.join([
                        'info point - meeting room - reception - shop - ',
                        'snack - studio'])}],
            'timestamp': '2020-04-27T13:00:00+00:00',
            'description': 'A human actually offline.'}
        embed_dict.update(self.init_method)
        return embed_dict

    @property
    def add_role_infos(self):
        """Return the result expected for test_add_role_infos."""
        embed_dict = {
            'footer': {'text': 'Created on'},
            'timestamp': '2020-04-27T15:30:00+00:00',
            'description': 'position: 1'}
        embed_dict.update(self.add_auth_channels)
        embed_dict['fields'].insert(0, {
            'inline': False, 'name': 'Members', 'value': 'Billy - Joe'})
        return embed_dict
