class ConfCommandsTestResult():
    """Class with ConfCommandsTest expected result - [(name, help), ...]."""

    @property
    def cog_guild(self):
        """Return the result expected for test_cog_guild."""
        return [
            ('guild', "Guild's stats -> #guild"),
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
    def cog_components(self):
        """Return the result expected for test_cog_components."""
        return [
            ('mem', "Infos of a member -> #mem id_or_name"), ]
