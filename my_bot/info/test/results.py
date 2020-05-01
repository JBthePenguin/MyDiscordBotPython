class GuildEmbedTestResult():
    """Class with GuildEmbedTest expected result."""

    @property
    def init_method(self):
        """Return the result expected for test_init."""
        return {
            'author': {
                'name': 'Guild Embed Test',
                'icon_url': 'https://url.com/icon.png'},
            'color': 1447446,
            'type': 'rich'}

    @property
    def add_stat(self):
        """Return the result expected for test_add_stat."""
        return [{'inline': True, 'name': 'Members', 'value': '5'}]

    @property
    def add_title_stats(self):
        """Return the result expected for test_add_title_stats."""
        return {
            'title': 'id: 6',
            'fields': [
                {'inline': True, 'name': 'Members', 'value': '6'},
                {'inline': True, 'name': 'Roles', 'value': '3'},
                {'inline': True, 'name': 'Emojis', 'value': '4'},
                {'inline': True, 'name': 'Channel Categories', 'value': '2'},
                {'inline': True, 'name': 'Channels', 'value': '7'},
                {'inline': True, 'name': 'Text Channels', 'value': '3'},
                {'inline': True, 'name': 'Voice Channels', 'value': '2'},
                {'inline': True, 'name': 'News Channels', 'value': '1'},
                {'inline': True, 'name': 'Store Channels', 'value': '1'}],
            'footer': {'text': 'Owner: Jean-Pierre'}}

    @property
    def add_title_objs(self):
        """Return the result expected for test_add_title_objs."""
        return {
            'title': 'Members',
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '1\n3\n0\n2\n4\n5'},
                {
                    'inline': True, 'name': 'Name',
                    'value': 'Al\nBilly\nJean-Pierre\nJoe\nJohn\nMike'}],
            'footer': {'text': 'Total: 6'}}

    @property
    def add_emojis(self):
        """Return the result expected for test_add_emojis."""
        return [
            {
                'inline': True, 'name': '\u200b',
                'value': '<:bad:20> bad\n\n<:strong:21> strong'},
            {
                'inline': True, 'name': '\u200b',
                'value': '<:cool:18> cool\n\n<:good:19> good'}]


class GuildShellTestResult():
    """Class with GuildShellTest expected result."""

    @property
    def add_list(self):
        """Return the result expected for test_add_list."""
        return {
            'guild': '\n'.join([
                '\n##########  Guild ##########',
                '- 6 - Full guild\n']),
            'owner': '\n'.join([
                '\n##########  Owner ##########',
                '- 0 - Jean-Pierre\n']),
            'objs': '\n'.join([
                '\n########## 6 Members ##########',
                '- 1 - Al',
                '- 3 - Billy',
                '- 0 - Jean-Pierre',
                '- 2 - Joe',
                '- 4 - John',
                '- 5 - Mike\n'])}

    @property
    def add_emojis(self):
        """Return the result expected for test_add_emojis."""
        return '\n'.join([
            '- <:cool:18> cool - <:good:19> good - <:bad:20> bad ',
            '- <:strong:21> strong '])

    @property
    def add_type_chans(self):
        """Return the result expected for test_add_type_chans."""
        return '\n'.join([
            '### 2 Voice Channels',
            '- 14 - snack',
            '- 15 - studio\n'])

    @property
    def add_cats_chans(self):
        """Return the result expected for test_add_cats_chans."""
        return '\n'.join([
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

    @property
    def add_infos(self):
        """Return the result expected for test_add_infos."""
        result = ''
        # guild owner members
        for value in self.add_list.values():
            result += value
        # roles categories
        result += '\n'.join([
            '\n########## 3 Roles ##########',
            '- 6 - @everyone',
            '- 7 - admin',
            '- 8 - staff',
            '\n########## 2 Channel Categories ##########',
            '- 9 - 1st floor',
            '- 10 - 2nd floor\n'])
        # channels
        result += '\n'.join([
            '\n########## 7 Channels ##########',
            '- 17 - boss office',
            '- 12 - info point',
            '- 16 - meeting room',
            '- 11 - reception',
            '- 13 - shop',
            '- 14 - snack',
            '- 15 - studio\n'])
        # text voice news store CHANNELS
        result += '\n'.join([
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
            '- 13 - shop\n'])
        # emojis channels by categories
        result += '\n'.join([
            '\n########## 4 Emojis ##########',
            self.add_emojis])
        result += self.add_cats_chans
        return result


class MakeObjsEmbedTestResult():
    """Class with MakeObjsEmbedTest expected result."""

    @property
    def empty_list(self):
        """Return the result expected for test_empty_list."""
        embed_dict = GuildEmbedTestResult().init_method
        embed_dict['title'] = 'No member'
        return embed_dict

    @property
    def not_empty_list(self):
        """Return the result expected for test_not_empty_list (embed dict)."""
        embed_dict = GuildEmbedTestResult().init_method
        embed_dict.update(GuildEmbedTestResult().add_title_objs)
        return embed_dict


class InfoGuildCommandsTestResult():
    """Class with InfoGuildCommandsTest expected result."""

    @property
    def base_result(self):
        """Return a base for result, a dict with author(name, icon_url),
        color and type."""
        icon_url = 'https://cdn.discordapp.com/icons/6/icon.png.webp?size=1024'
        return {
            'author': {'name': 'Full guild', 'icon_url': icon_url},
            'color': 1447446,
            'type': 'rich'}

    @property
    def init_method(self):
        """Return the result expected for test_init - [(name, help), ...]."""
        return [
            ('guild', "Guild's stats -> #guild"),
            ('owner', 'The Owner-> #owner'),
            ('mems', 'All members -> #mems'),
            ('roles', 'All roles -> #roles'),
            ('cats', "All channel's categories -> #cats"),
            ('chans', 'All channels -> #chans'),
            ('tchans', 'All text channels -> #tchans'),
            ('vchans', 'All voice channels -> #vchans'),
            ('nchans', 'All news channels -> #nchans'),
            ('schans', 'All store channels -> #schans'),
            ('emos', 'All emojis -> #emos'),
            ('shell', 'Infos in shell -> #shell')]

    @property
    def guild(self):
        """Return the result expected for test_guild (embed dict)."""
        embed_dict = GuildEmbedTestResult().add_title_stats
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def owner(self):
        """Return the result expected for test_owner (embed dict)."""
        embed_dict = {
            'title': 'Owner',
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '0'},
                {'inline': True, 'name': 'Name', 'value': 'Jean-Pierre'}],
            'footer': {'text': 'Total: 1'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def members(self):
        """Return the result expected for test_members (embed dict)."""
        embed_dict = GuildEmbedTestResult().add_title_objs
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def roles(self):
        """Return the result expected for test_roles (embed dict)."""
        embed_dict = {
            'title': 'Roles',
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '6\n7\n8'},
                {
                    'inline': True, 'name': 'Name',
                    'value': '@everyone\nadmin\nstaff'}],
            'footer': {'text': 'Total: 3'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def categories(self):
        """Return the result expected for test_categories (embed dict)."""
        embed_dict = {
            'title': 'Channel Categories',
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '9\n10'},
                {
                    'inline': True, 'name': 'Name',
                    'value': '1st floor\n2nd floor'}],
            'footer': {'text': 'Total: 2'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def channels(self):
        """Return the result expected for test_channels (embed dict)."""
        embed_dict = {
            'title': 'Channels',
            'fields': [
                {
                    'inline': True, 'name': 'ID',
                    'value': '17\n12\n16\n11\n13\n14\n15'},
                {
                    'inline': True, 'name': 'Name',
                    'value': '\n'.join([
                        'boss office', 'info point', 'meeting room',
                        'reception', 'shop', 'snack', 'studio'])}],
            'footer': {'text': 'Total: 7'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def text_channels(self):
        """Return the result expected for test_text_channels (embed dict)."""
        embed_dict = {
            'title': 'Text Channels',
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '17\n16\n11'},
                {
                    'inline': True, 'name': 'Name',
                    'value': 'boss office\nmeeting room\nreception'}],
            'footer': {'text': 'Total: 3'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def voice_channels(self):
        """Return the result expected for test_voice_channels (embed dict)."""
        embed_dict = {
            'title': 'Voice Channels',
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '14\n15'},
                {'inline': True, 'name': 'Name', 'value': 'snack\nstudio'}],
            'footer': {'text': 'Total: 2'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def news_channels(self):
        """Return the result expected for test_news_channels (embed dict)."""
        embed_dict = {
            'title': 'News Channels',
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '12'},
                {'inline': True, 'name': 'Name', 'value': 'info point'}],
            'footer': {'text': 'Total: 1'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def store_channels(self):
        """Return the result expected for test_store_channels (embed dict)."""
        embed_dict = {
            'title': 'Store Channels',
            'fields': [
                {'inline': True, 'name': 'ID', 'value': '13'},
                {'inline': True, 'name': 'Name', 'value': 'shop'}],
            'footer': {'text': 'Total: 1'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def emojis(self):
        """Return the result expected for test_emojis (embed dict)."""
        embed_dict = {
            'title': 'Emojis',
            'fields': GuildEmbedTestResult().add_emojis,
            'footer': {'text': 'Total: 4'}}
        embed_dict.update(self.base_result)
        return embed_dict

    @property
    def shell_info(self):
        """Return the result expected for test_shell_info (string)."""
        return GuildShellTestResult().add_infos


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


class InfoComponentsCommandsTestResult():
    """Class with InfoComponentsCommandsTest expected result."""

    @property
    def init_method(self):
        """Return the result expected for test_init - [(name, help), ...]."""
        return [
            ('mem', "Infos of a member -> #mem id_or_name"), ]

    @property
    def member(self):
        """Return the result expected for test_member - embed or not found."""
        base_result = {
            'footer': {'text': 'Member since'}, 'color': 0,
            'timestamp': '2020-04-27T13:00:00+00:00', 'type': 'rich',
            'description': 'A human actually offline.', }
        id_result = {
            'author': {
                'name': 'id: 1',
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
            'title': 'Al'}
        id_result.update(base_result)
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
