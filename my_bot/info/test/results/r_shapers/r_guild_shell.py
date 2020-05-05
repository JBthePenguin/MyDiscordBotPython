# GuildShellTest expected results
G_SHELL_RESULTS = {}


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
            '- <:strong:21> strong \n'])

    @property
    def add_type_chans(self):
        """Return the result expected for test_add_type_chans."""
        return '\n'.join([
            '### 2 Voice Channels',
            '- 14 - snack',
            '- 15 - studio\n'])
