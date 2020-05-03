from .r_shapers import GuildEmbedTestResult, GuildShellTestResult


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
