from my_tester.com_parser import ArgumentParserTestCase
from my_bot.info.test import INFO_TESTS

EVENT_TESTS = []

groups = [('info', INFO_TESTS), ('event', EVENT_TESTS)]
ArgumentParserTestCase(groups)
