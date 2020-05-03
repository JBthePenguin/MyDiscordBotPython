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
    embed_base_result = {  # author(name, icon_url), color, type
        'author': {'name': 'Full guild', 'icon_url': ''.join([
            'https://cdn.discordapp.com/icons/',
            '6/icon.png.webp?size=1024'])},
        'color': 1447446,
        'type': 'rich'}

    @property
    def guild(self):
        """Return the result expected for test_guild (embed dict)."""
        embed_dict = GuildEmbedTestResult().add_title_stats
        embed_dict.update(self.embed_base_result)
        return embed_dict

    def get_embed_dict(self, title, values, total):
        """Return embed dict {title, fields, footer} and updated with base."""
        embed_dict = {
            'title': title,
            'fields': [
                {'inline': True, 'name': 'ID', 'value': values[0]},
                {'inline': True, 'name': 'Name', 'value': values[1]}],
            'footer': {'text': f'Total: {total}'}}
        embed_dict.update(self.embed_base_result)
        return embed_dict

    @property
    def owner(self):
        """Return the result expected for test_owner (embed dict)."""
        return self.get_embed_dict('Owner', ('0', 'Jean-Pierre'), '1')

    @property
    def members(self):
        """Return the result expected for test_members (embed dict)."""
        embed_dict = GuildEmbedTestResult().add_title_objs
        embed_dict.update(self.embed_base_result)
        return embed_dict

    @property
    def roles(self):
        """Return the result expected for test_roles (embed dict)."""
        return self.get_embed_dict(
            'Roles', ('6\n7\n8', '@everyone\nadmin\nstaff'), '3')

    @property
    def categories(self):
        """Return the result expected for test_categories (embed dict)."""
        return self.get_embed_dict(
            'Channel Categories', ('9\n10', '1st floor\n2nd floor'), '2')

    @property
    def channels(self):
        """Return the result expected for test_channels (embed dict)."""
        return self.get_embed_dict(
            'Channels', ('17\n12\n16\n11\n13\n14\n15', '\n'.join([
                'boss office', 'info point', 'meeting room',
                'reception', 'shop', 'snack', 'studio'])), '7')

    @property
    def text_channels(self):
        """Return the result expected for test_text_channels (embed dict)."""
        return self.get_embed_dict('Text Channels', (
            '17\n16\n11', 'boss office\nmeeting room\nreception'), '3')

    @property
    def voice_channels(self):
        """Return the result expected for test_voice_channels (embed dict)."""
        return self.get_embed_dict(
            'Voice Channels', ('14\n15', 'snack\nstudio'), '2')

    @property
    def news_channels(self):
        """Return the result expected for test_news_channels (embed dict)."""
        return self.get_embed_dict('News Channels', ('12', 'info point'), '1')

    @property
    def store_channels(self):
        """Return the result expected for test_store_channels (embed dict)."""
        return self.get_embed_dict('Store Channels', ('13', 'shop'), '1')

    @property
    def emojis(self):
        """Return the result expected for test_emojis (embed dict)."""
        embed_dict = {
            'title': 'Emojis',
            'fields': GuildEmbedTestResult().add_emojis,
            'footer': {'text': 'Total: 4'}}
        embed_dict.update(self.embed_base_result)
        return embed_dict

    @property
    def shell_info(self):
        """Return the result expected for test_shell_info (string)."""
        return GuildShellTestResult().add_infos
