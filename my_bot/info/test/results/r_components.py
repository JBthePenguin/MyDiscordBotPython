class InfoComponentsCommandsTestResult():
    """Class with InfoComponentsCommandsTest expected result."""

    @property
    def member(self):
        """Return the result expected for test_member - embed or not found."""
        base_result = {
            'footer': {'text': 'Member since'}, 'color': 0,
            'timestamp': '2020-04-27T13:00:00+00:00', 'type': 'rich',
            'description': "A human actually offline.", }
        id_result = {
            'author': {
                'name': 'id: 0',
                'icon_url': 'https://url.com/avatar.png'},
            'fields': [
                {
                    'inline': False, 'name': 'Roles',
                    'value': '@everyone - admin'},
                {
                    'inline': False, 'name': 'Channels allowed to view',
                    'value': "All"}],
            'title': 'Jean-Pierre'}
        id_result.update(base_result)
        id_result['description'] += " He's the owner."
        name_result = {
            'author': {
                'name': 'id: 2',
                'icon_url': 'https://url.com/avatar.png'},
            'fields': [
                {
                    'inline': False, 'name': 'Roles',
                    'value': '@everyone - staff'},
                {
                    'inline': False, 'name': 'Channels allowed to view',
                    'value': ''.join([
                        'info point - meeting room - reception - shop - ',
                        'snack - studio'])}],
            'title': 'Joe'}
        name_result.update(base_result)
        return {
            'id': id_result,
            'name': name_result,
            'no_id': 'Member with id 12 not founded.',
            'no_name': 'Member with name Tom not founded.'}

    @property
    def role(self):
        """Return the result expected for test_role - embed or not found."""
        base_result = {
            'footer': {'text': 'Member since'}, 'color': 0,
            'timestamp': '2020-04-27T13:00:00+00:00', 'type': 'rich',
            'description': "A human actually offline.", }
        id_result = {
            'author': {
                'name': 'id: 0',
                'icon_url': 'https://url.com/avatar.png'},
            'fields': [
                {
                    'inline': False, 'name': 'Roles',
                    'value': '@everyone - admin'},
                {
                    'inline': False, 'name': 'Channels allowed to view',
                    'value': ''.join([
                        '1st floor - 2nd floor - boss office - info point - ',
                        'meeting room - reception - shop - snack - studio'])}],
            'title': 'Jean-Pierre'}
        id_result.update(base_result)
        id_result['description'] += " He's the owner."
        name_result = {
            'author': {
                'name': 'id: 2',
                'icon_url': 'https://url.com/avatar.png'},
            'fields': [
                {
                    'inline': False, 'name': 'Roles',
                    'value': '@everyone - staff'},
                {
                    'inline': False, 'name': 'Channels allowed to view',
                    'value': ''.join([
                        'info point - meeting room - reception - shop - ',
                        'snack - studio'])}],
            'title': 'Joe'}
        name_result.update(base_result)
        return {
            'id': id_result,
            'name': name_result,
            'no_id': 'Member with id 12 not founded.',
            'no_name': 'Member with name Tom not founded.'}
