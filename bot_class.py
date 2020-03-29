from info_team_bot.bot_class import InfoTeamBot
from calendar_bot.bot_class import CalendarBot


class FullBot(InfoTeamBot):

    def __init__(self):
        super().__init__()

    def run(self, token):
        super().run(token)
