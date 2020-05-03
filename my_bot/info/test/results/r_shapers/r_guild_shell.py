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
        # roles emojis categories
        result += '\n'.join([
            '\n########## 3 Roles ##########',
            '- 6 - @everyone',
            '- 7 - admin',
            '- 8 - staff',
            '\n########## 4 Emojis ##########',
            self.add_emojis,
            '########## 2 Channel Categories ##########',
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
        # channels by categories
        result += self.add_cats_chans
        return result
