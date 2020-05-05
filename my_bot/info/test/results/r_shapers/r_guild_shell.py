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
